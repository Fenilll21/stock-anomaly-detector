"""
src/ui/header.py
----------------
Page title and company header components.
"""

import streamlit as st


def render_page_header() -> None:
    st.markdown(
        """
        <div style='margin-bottom:1.5rem;'>
            <div class='page-title'>
                Stock Market <em>Anomaly Radar</em>
            </div>
            <div class='page-subtitle'>
                Detect unusual price &amp; volume behaviour —
                Z-Score analysis + Isolation Forest
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_company_header(info: dict, ticker: str, summary: dict) -> None:
    _render_company_name(info, ticker)
    st.markdown("<hr style='margin:0.75rem 0'/>", unsafe_allow_html=True)
    _render_kpi_cards(summary)
    st.markdown("<hr style='margin:1rem 0'/>", unsafe_allow_html=True)


def _render_company_name(info: dict, ticker: str) -> None:
    st.markdown(
        f"""
        <div>
            <div class='company-name'>
                {info['name']}
                <span class='ticker-badge'>{ticker}</span>
            </div>
            <div class='company-meta'>
                {info['sector']}
                <span class='meta-sep'>·</span>
                {info['exchange']}
                <span class='meta-sep'>·</span>
                {info['currency']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_kpi_cards(summary: dict) -> None:
    st.markdown("<p class='section-label'>Overview</p>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Trading Days",    summary["total_days"])
    c2.metric("Total Anomalies", summary["total_anomalies"],
              delta=f"{summary['anomaly_rate']}% of days", delta_color="off")
    c3.metric("Z-Score Only",    summary["zscore_only"])
    c4.metric("IForest Only",    summary["iforest_only"])
    c5.metric("Both Methods",    summary["both_methods"])
    c6.metric("Worst Return",    f"{summary['worst_return']}%", delta_color="inverse")