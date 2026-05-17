"""
src/ui/charts.py
----------------
Chart tabs, anomaly data table, and empty-state placeholder for the
Stock Market Anomaly Detector.

Functions
---------
render_chart_tabs(df, ticker)
    Five analysis tabs with Plotly charts. Call when results exist.

render_anomaly_table(df, ticker)
    Expandable raw anomaly dataframe + CSV download button.

render_empty_state()
    Placeholder UI shown before the first analysis run.
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

_COLUMN_FORMATS = {
    "Open":         "${:.2f}",
    "High":         "${:.2f}",
    "Low":          "${:.2f}",
    "Close":        "${:.2f}",
    "Volume":       "{:,.0f}",
    "Daily_Return": "{:.2f}%",
    "Price_Range":  "{:.2f}%",
}

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
        Processed dataframe from run_anomaly_detection().
    ticker : str
        Upper-cased ticker symbol e.g. "AAPL".
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
        st.plotly_chart(
            plot_price_anomalies(df, ticker),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with tab2:
        _chart_desc(
            "Absolute Z-scores per feature over time. "
            "The shaded band marks the anomaly threshold zone."
        )
        st.plotly_chart(
            plot_zscore_heatmap(df),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with tab3:
        _chart_desc(
            "Isolation Forest anomaly scores — higher = more anomalous. "
            "Red bars were flagged by the model."
        )
        st.plotly_chart(
            plot_iforest_scores(df),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with tab4:
        _chart_desc(
            "Daily return distribution split by normal vs. anomalous days. "
            "Anomalies cluster in the tails."
        )
        st.plotly_chart(
            plot_return_distribution(df),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with tab5:
        _chart_desc(
            "Each point is a trading day in feature space. "
            "Colour encodes which detector(s) flagged it."
        )
        st.plotly_chart(
            plot_anomaly_scatter(df),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    st.markdown("<br/>", unsafe_allow_html=True)


def render_anomaly_table(df: pd.DataFrame, ticker: str) -> None:
    """
    Expandable raw anomaly dataframe with CSV download.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain an Is_Anomaly boolean column.
    ticker : str
        Used for the CSV filename.
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
            height=360,
        )

        col_dl, col_rest = st.columns([1.5, 8.5])
        with col_dl:
            csv = anomaly_df.reset_index().to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇  Download CSV",
                data=csv,
                file_name=f"{ticker}_anomalies.csv",
                mime="text/csv",
            )


def render_empty_state() -> None:
    """
    Placeholder shown before the first analysis run.
    """
    st.markdown(
        """
        <div class='empty-state'>
            <span class='empty-state-icon'>📡</span>
            <h3>Ready to scan the market</h3>
            <p>Enter a ticker and hit <strong>Run Analysis</strong> above to begin.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p class='example-section-title'>Suggested tickers to try</p>",
        unsafe_allow_html=True,
    )

    rows = ""
    for t, a, w in zip(
        _EXAMPLE_TICKERS["Ticker"],
        _EXAMPLE_TICKERS["Asset"],
        _EXAMPLE_TICKERS["Why"],
    ):
        rows += f"""
        <tr>
            <td><span class='ticker-badge'>{t}</span></td>
            <td style='color:#1c2128;font-weight:500;'>{a}</td>
            <td>{w}</td>
        </tr>"""

    st.markdown(
        f"""
        <table class='example-table'>
            <thead>
                <tr>
                    <th>Ticker</th>
                    <th>Asset</th>
                    <th>Why try it</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )


# ── Private helpers ───────────────────────────────────────────────────────────

def _chart_desc(text: str) -> None:
    """Styled description line above each chart."""
    st.markdown(
        f"<p class='chart-desc'>{text}</p>",
        unsafe_allow_html=True,
    )