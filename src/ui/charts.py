"""
src/ui/charts.py
----------------
Chart tabs, anomaly data table, and empty-state placeholder for the
Stock Market Anomaly Detector.

Functions
---------
render_chart_tabs(df, ticker)
    Renders the five analysis tabs, each with a Plotly chart and a
    short description. Call only when results are available.

render_anomaly_table(df, ticker)
    Renders the expandable raw anomaly dataframe with a CSV download
    button. Call only when results are available.

render_empty_state()
    Renders the placeholder UI shown before the first analysis run,
    including the suggested tickers table.

Usage
-----
    from src.ui.charts import render_chart_tabs, render_anomaly_table, render_empty_state

    if st.session_state["results"]:
        render_chart_tabs(df, ticker)
        render_anomaly_table(df, ticker)
    else:
        render_empty_state()
"""

import pandas as pd
import streamlit as st

from src.visualizer import (
    plot_price_anomalies,
    plot_zscore_heatmap,
    plot_iforest_scores,
    plot_return_distribution,
    plot_anomaly_scatter,
)

# Columns shown in the raw anomaly table
_ANOMALY_COLUMNS = [
    "Open", "High", "Low", "Close", "Volume",
    "Daily_Return", "Price_Range",
    "ZScore_Anomaly", "IForest_Anomaly", "Anomaly_Type",
]

# Format spec for the styled dataframe
_COLUMN_FORMATS = {
    "Open":         "${:.2f}",
    "High":         "${:.2f}",
    "Low":          "${:.2f}",
    "Close":        "${:.2f}",
    "Volume":       "{:,.0f}",
    "Daily_Return": "{:.2f}%",
    "Price_Range":  "{:.2f}%",
}

# Suggested tickers shown in the empty state
_EXAMPLE_TICKERS = {
    "Ticker": ["AAPL", "TSLA", "NVDA", "BTC-USD", "SPY",  "AMZN"],
    "Asset":  ["Apple", "Tesla", "NVIDIA", "Bitcoin", "S&P 500 ETF", "Amazon"],
    "Why": [
        "Blue chip, steady baseline",
        "High volatility — rich anomaly set",
        "AI boom — dramatic 2023–24 run",
        "Crypto — extreme tail behaviour",
        "Broad market benchmark",
        "E-commerce mega-cap",
    ],
}


def render_chart_tabs(df: pd.DataFrame, ticker: str) -> None:
    """
    Render the five analysis tabs with Plotly charts.

    Parameters
    ----------
    df : pd.DataFrame
        Processed dataframe returned by run_anomaly_detection().
    ticker : str
        Upper-cased ticker symbol, e.g. ``"AAPL"``.
    """
    st.markdown("<p class='section-label'>Analysis</p>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Price & Volume",
        "Z-Score",
        "Isolation Forest",
        "Return Distribution",
        "Feature Space",
    ])

    with tab1:
        _chart_desc(
            "Candlestick chart with anomaly markers overlaid. "
            "Red volume bars indicate anomalous sessions."
        )
        st.plotly_chart(plot_price_anomalies(df, ticker), use_container_width=True)

    with tab2:
        _chart_desc(
            "Absolute Z-scores per feature over time. "
            "The shaded band marks the anomaly threshold zone."
        )
        st.plotly_chart(plot_zscore_heatmap(df), use_container_width=True)

    with tab3:
        _chart_desc(
            "Isolation Forest anomaly scores — higher values indicate more "
            "anomalous sessions. Red bars were flagged by the model."
        )
        st.plotly_chart(plot_iforest_scores(df), use_container_width=True)

    with tab4:
        _chart_desc(
            "Daily return distribution split by normal vs. anomalous days. "
            "Anomalies cluster in the tails."
        )
        st.plotly_chart(plot_return_distribution(df), use_container_width=True)

    with tab5:
        _chart_desc(
            "Each point is a trading day plotted in feature space. "
            "Colour encodes which detector(s) flagged it."
        )
        st.plotly_chart(plot_anomaly_scatter(df), use_container_width=True)

    st.markdown("<br/>", unsafe_allow_html=True)


def render_anomaly_table(df: pd.DataFrame, ticker: str) -> None:
    """
    Render the expandable raw anomaly dataframe and CSV download button.

    Parameters
    ----------
    df : pd.DataFrame
        Processed dataframe returned by run_anomaly_detection(). Must
        contain an ``Is_Anomaly`` boolean column.
    ticker : str
        Upper-cased ticker symbol used for the CSV filename.
    """
    anomaly_df = (
        df[df["Is_Anomaly"]][_ANOMALY_COLUMNS]
        .sort_index(ascending=False)
    )
    n = len(anomaly_df)

    with st.expander(f"🔍  Raw Anomaly Data  ·  {n} records"):
        st.markdown(
            f"<p class='section-label'>{n} anomalous trading days</p>",
            unsafe_allow_html=True,
        )
        st.dataframe(
            anomaly_df.style.format(_COLUMN_FORMATS),
            use_container_width=True,
            height=380,
        )

        csv = anomaly_df.reset_index().to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇  Download CSV",
            data=csv,
            file_name=f"{ticker}_anomalies.csv",
            mime="text/csv",
        )


def render_empty_state() -> None:
    """
    Render the placeholder shown before the first analysis run.

    Displays a centred call-to-action card and a table of suggested
    tickers to help new users get started quickly.
    """
    st.markdown(
        """
        <div class='empty-state'>
            <span class='empty-state-icon'>📡</span>
            <h3>Ready to scan the market</h3>
            <p>Configure your ticker symbol and parameters in the sidebar,
               then hit <strong>Run Analysis</strong> to begin.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p class='example-section-title'>Suggested tickers</p>",
        unsafe_allow_html=True,
    )
    st.dataframe(
        pd.DataFrame(_EXAMPLE_TICKERS),
        use_container_width=True,
        hide_index=True,
    )


# ── Private helpers ───────────────────────────────────────────────────────────

def _chart_desc(text: str) -> None:
    """Render a styled chart description above each Plotly chart."""
    st.markdown(
        f"<p class='chart-desc'>{text}</p>",
        unsafe_allow_html=True,
    )