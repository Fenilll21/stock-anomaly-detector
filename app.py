"""
app.py
------
Main Streamlit dashboard for the Stock Market Anomaly Detector.

Layout
------
Sidebar  : all user-configurable parameters
Main area:
  ├── Ticker info header + KPI metric cards
  ├── Tab 1 — Price & Volume chart with anomaly overlay
  ├── Tab 2 — Z-Score analysis
  ├── Tab 3 — Isolation Forest scores
  ├── Tab 4 — Return distribution
  ├── Tab 5 — Feature space scatter
  └── Raw anomaly data table (expandable)

Run with:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
from datetime import date, timedelta

from src.data_fetcher    import fetch_stock_data, get_ticker_info, validate_date_range
from src.anomaly_detector import run_anomaly_detection, get_anomaly_summary
from src.visualizer      import (
    plot_price_anomalies,
    plot_zscore_heatmap,
    plot_iforest_scores,
    plot_return_distribution,
    plot_anomaly_scatter,
)

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Anomaly Detector",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS tweaks ────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Metric card value size */
    [data-testid="stMetricValue"] { font-size: 1.6rem; }
    /* Thin divider */
    hr { border-top: 1px solid rgba(255,255,255,0.1); margin: 0.5rem 0; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Sidebar — user controls ─────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Configuration")
    st.markdown("---")

    # ── Ticker ────────────────────────────────────────────────────────────
    st.subheader("📌 Stock Selection")
    ticker = st.text_input(
        "Ticker Symbol",
        value="AAPL",
        max_chars=10,
        help="Enter any valid Yahoo Finance ticker, e.g. TSLA, NVDA, BTC-USD",
    ).upper().strip()

    # Quick-pick buttons
    st.caption("Quick picks:")
    cols = st.columns(4)
    quick_tickers = ["AAPL", "TSLA", "NVDA", "MSFT"]
    for col, qt in zip(cols, quick_tickers):
        if col.button(qt, use_container_width=True):
            ticker = qt

    st.markdown("---")

    # ── Date range ────────────────────────────────────────────────────────
    st.subheader("📅 Date Range")
    default_end   = date.today()
    default_start = default_end - timedelta(days=365 * 2)   # 2 years default

    start_date = st.date_input("Start Date", value=default_start, max_value=default_end)
    end_date   = st.date_input("End Date",   value=default_end,   max_value=default_end)

    st.markdown("---")

    # ── Detector parameters ───────────────────────────────────────────────
    st.subheader("🔬 Detector Settings")

    zscore_threshold = st.slider(
        "Z-Score Threshold",
        min_value=1.5,
        max_value=5.0,
        value=2.5,
        step=0.1,
        help=(
            "Days whose |Z-score| exceeds this value are flagged. "
            "Lower = more sensitive (more anomalies flagged)."
        ),
    )

    contamination = st.slider(
        "Isolation Forest Contamination",
        min_value=0.01,
        max_value=0.20,
        value=0.05,
        step=0.01,
        format="%.2f",
        help=(
            "Expected proportion of anomalies in the dataset (0.01 – 0.20). "
            "Higher = Isolation Forest flags more points as anomalous."
        ),
    )

    st.markdown("---")

    # ── Run button ────────────────────────────────────────────────────────
    run_button = st.button("🚀 Run Analysis", use_container_width=True, type="primary")

    st.markdown("---")
    st.caption(
        "**Stock Market Anomaly Detector**  \n"
        "Z-Score + Isolation Forest  \n"
        "Data via [yfinance](https://github.com/ranaroussi/yfinance)"
    )


# ── Main area ────────────────────────────────────────────────────────────────
st.title("📈 Stock Market Anomaly Detector")
st.markdown(
    "Detect unusual price and volume behaviour using **Z-Score analysis** "
    "and **Isolation Forest** — adjust the parameters in the sidebar and click **Run Analysis**."
)

# ── Session-state initialisation ─────────────────────────────────────────────
# We store results in st.session_state so the page doesn't reset on widget interaction
if "results" not in st.session_state:
    st.session_state["results"] = None
if "error"   not in st.session_state:
    st.session_state["error"]   = None


# ── Run pipeline when button is pressed ──────────────────────────────────────
if run_button:
    st.session_state["error"]   = None
    st.session_state["results"] = None

    try:
        # Validate inputs before hitting the API
        validate_date_range(str(start_date), str(end_date))

        with st.spinner(f"Fetching data for **{ticker}**…"):
            df   = fetch_stock_data(ticker, str(start_date), str(end_date))
            info = get_ticker_info(ticker)

        with st.spinner("Running anomaly detection…"):
            df      = run_anomaly_detection(df, zscore_threshold, contamination)
            summary = get_anomaly_summary(df)

        # Persist results across reruns
        st.session_state["results"] = {
            "df":      df,
            "info":    info,
            "summary": summary,
            "ticker":  ticker,
        }

    except ValueError as ve:
        st.session_state["error"] = str(ve)
    except Exception as ex:
        st.session_state["error"] = f"Unexpected error: {ex}"


# ── Render error banner ───────────────────────────────────────────────────────
if st.session_state["error"]:
    st.error(f"❌ {st.session_state['error']}")


# ── Render results ────────────────────────────────────────────────────────────
if st.session_state["results"]:
    res     = st.session_state["results"]
    df      = res["df"]
    info    = res["info"]
    summary = res["summary"]
    ticker  = res["ticker"]

    # ── Company header ─────────────────────────────────────────────────────
    st.markdown(f"### {info['name']}  `{ticker}`")
    st.caption(f"Sector: {info['sector']} · Exchange: {info['exchange']} · Currency: {info['currency']}")
    st.markdown("---")

    # ── KPI metric cards ──────────────────────────────────────────────────
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("📆 Trading Days",  summary["total_days"])
    c2.metric("🚨 Total Anomalies", summary["total_anomalies"],
              delta=f"{summary['anomaly_rate']}% of days",
              delta_color="off")
    c3.metric("🟡 Z-Score Only",  summary["zscore_only"])
    c4.metric("🟣 IForest Only",  summary["iforest_only"])
    c5.metric("🔴 Both Methods",  summary["both_methods"])
    c6.metric("📉 Worst Return",  f"{summary['worst_return']}%",
              delta_color="inverse")

    st.markdown("---")

    # ── Chart tabs ────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Price & Volume",
        "📐 Z-Score Analysis",
        "🌲 Isolation Forest",
        "📉 Return Distribution",
        "🔵 Feature Space",
    ])

    with tab1:
        st.markdown(
            "Candlestick chart with **anomaly markers** overlaid. "
            "Red volume bars indicate anomalous days."
        )
        st.plotly_chart(plot_price_anomalies(df, ticker), use_container_width=True)

    with tab2:
        st.markdown(
            "Absolute Z-scores for each feature over time. "
            "The red band marks the anomaly zone above the configured threshold."
        )
        st.plotly_chart(plot_zscore_heatmap(df), use_container_width=True)

    with tab3:
        st.markdown(
            "Isolation Forest anomaly scores (higher = more anomalous). "
            "Red bars were flagged by the model as anomalies."
        )
        st.plotly_chart(plot_iforest_scores(df), use_container_width=True)

    with tab4:
        st.markdown(
            "Distribution of daily returns split by normal vs anomalous days. "
            "Anomalies tend to cluster in the tails."
        )
        st.plotly_chart(plot_return_distribution(df), use_container_width=True)

    with tab5:
        st.markdown(
            "Each dot is a trading day plotted in feature space. "
            "Colour indicates which detector(s) flagged it."
        )
        st.plotly_chart(plot_anomaly_scatter(df), use_container_width=True)

    # ── Raw anomaly table ─────────────────────────────────────────────────
    with st.expander("🔍 View Raw Anomaly Data"):
        anomaly_df = (
            df[df["Is_Anomaly"]]
            [[
                "Open", "High", "Low", "Close", "Volume",
                "Daily_Return", "Price_Range",
                "ZScore_Anomaly", "IForest_Anomaly", "Anomaly_Type",
            ]]
            .sort_index(ascending=False)
        )

        st.markdown(f"**{len(anomaly_df)} anomalous trading days detected:**")
        st.dataframe(
            anomaly_df.style.format({
                "Open":         "${:.2f}",
                "High":         "${:.2f}",
                "Low":          "${:.2f}",
                "Close":        "${:.2f}",
                "Volume":       "{:,.0f}",
                "Daily_Return": "{:.2f}%",
                "Price_Range":  "{:.2f}%",
            }),
            use_container_width=True,
            height=400,
        )

        # Download button
        csv = anomaly_df.reset_index().to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download anomalies as CSV",
            data=csv,
            file_name=f"{ticker}_anomalies.csv",
            mime="text/csv",
        )

else:
    # ── Placeholder when no results yet ──────────────────────────────────
    st.info(
        "👈 Configure your ticker and parameters in the sidebar, then click **Run Analysis**.",
        icon="ℹ️",
    )

    # Show example tickers for inspiration
    st.markdown("#### Example tickers to try")
    example_data = {
        "Ticker":    ["AAPL", "TSLA", "NVDA", "BTC-USD", "SPY",  "AMZN"],
        "Asset":     ["Apple", "Tesla", "NVIDIA", "Bitcoin", "S&P 500 ETF", "Amazon"],
        "Why":       [
            "Blue chip, steady",
            "High volatility — lots of anomalies",
            "AI boom — dramatic 2023–24",
            "Crypto — extreme behaviour",
            "Market benchmark",
            "E-commerce giant",
        ],
    }
    st.dataframe(pd.DataFrame(example_data), use_container_width=True, hide_index=True)
