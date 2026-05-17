"""
src/ui/charts.py
----------------
Chart tabs, anomaly table, and empty state.
"""

import pandas as pd
import streamlit as st

from src.visualizer import (
    plot_price_anomalies, plot_zscore_heatmap,
    plot_iforest_scores, plot_return_distribution, plot_anomaly_scatter,
)

_ANOMALY_COLUMNS = [
    "Open", "High", "Low", "Close", "Volume",
    "Daily_Return", "Price_Range",
    "ZScore_Anomaly", "IForest_Anomaly", "Anomaly_Type",
]
_COLUMN_FORMATS = {
    "Open": "${:.2f}", "High": "${:.2f}", "Low": "${:.2f}", "Close": "${:.2f}",
    "Volume": "{:,.0f}", "Daily_Return": "{:.2f}%", "Price_Range": "{:.2f}%",
}
_EXAMPLE_TICKERS = {
    "Ticker": ["AAPL", "TSLA", "NVDA", "BTC-USD", "SPY", "AMZN"],
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
_PLOTLY_CFG = {"displayModeBar": False}


def render_chart_tabs(df: pd.DataFrame, ticker: str) -> None:
    st.markdown("<p class='section-label'>Analysis</p>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Price & Volume", "Z-Score",
        "Isolation Forest", "Return Distribution", "Feature Space",
    ])
    with tab1:
        _desc("Candlestick with anomaly markers. Red volume bars = anomalous sessions.")
        st.plotly_chart(plot_price_anomalies(df, ticker), use_container_width=True, config=_PLOTLY_CFG)
    with tab2:
        _desc("Absolute Z-scores per feature. Shaded band = anomaly threshold zone.")
        st.plotly_chart(plot_zscore_heatmap(df), use_container_width=True, config=_PLOTLY_CFG)
    with tab3:
        _desc("Isolation Forest scores — higher = more anomalous. Red bars were flagged.")
        st.plotly_chart(plot_iforest_scores(df), use_container_width=True, config=_PLOTLY_CFG)
    with tab4:
        _desc("Daily return distribution: normal vs anomalous. Anomalies cluster in the tails.")
        st.plotly_chart(plot_return_distribution(df), use_container_width=True, config=_PLOTLY_CFG)
    with tab5:
        _desc("Feature space: each dot is a trading day. Colour = detector(s) that flagged it.")
        st.plotly_chart(plot_anomaly_scatter(df), use_container_width=True, config=_PLOTLY_CFG)
    st.markdown("<br/>", unsafe_allow_html=True)


def render_anomaly_table(df: pd.DataFrame, ticker: str) -> None:
    anomaly_df = df[df["Is_Anomaly"]][_ANOMALY_COLUMNS].sort_index(ascending=False)
    n = len(anomaly_df)
    with st.expander(f"🔍  Raw Anomaly Data  ·  {n} records"):
        st.markdown(f"<p class='section-label'>{n} anomalous trading days</p>", unsafe_allow_html=True)
        st.dataframe(anomaly_df.style.format(_COLUMN_FORMATS), use_container_width=True, height=360)
        col_dl, _ = st.columns([1.5, 8.5])
        with col_dl:
            csv = anomaly_df.reset_index().to_csv(index=False).encode("utf-8")
            st.download_button("⬇  Download CSV", data=csv,
                               file_name=f"{ticker}_anomalies.csv", mime="text/csv")


def render_empty_state() -> None:
    st.markdown(
        """
        <div class='empty-state'>
            <span class='empty-state-icon'>📡</span>
            <h3>Ready to scan the market</h3>
            <p>Open the sidebar, enter a ticker and hit Run Analysis to begin.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<p class='example-section-title'>Suggested tickers</p>", unsafe_allow_html=True)
    rows = "".join(
        f"<tr><td><span class='ticker-badge'>{t}</span></td>"
        f"<td style='color:#a1a1aa;font-weight:500'>{a}</td>"
        f"<td>{w}</td></tr>"
        for t, a, w in zip(
            _EXAMPLE_TICKERS["Ticker"],
            _EXAMPLE_TICKERS["Asset"],
            _EXAMPLE_TICKERS["Why"],
        )
    )
    st.markdown(
        f"""<table class='example-table'>
            <thead><tr><th>Ticker</th><th>Asset</th><th>Why try it</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>""",
        unsafe_allow_html=True,
    )


def _desc(text: str) -> None:
    st.markdown(f"<p class='chart-desc'>{text}</p>", unsafe_allow_html=True)