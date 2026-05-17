"""
src/ui/header.py
----------------
Page-level and results-level header components for the Stock Market
Anomaly Detector.

Functions
---------
render_page_header()
    App title + subtitle. Call once, right after inject_styles().

render_company_header(info, ticker, summary)
    Company name, ticker badge, sector metadata, divider, and the
    six KPI metric cards. Call only when results are available.
"""

import streamlit as st


def render_page_header() -> None:
    """
    Render the app title and one-line description.
    """
    st.markdown(
        """
        <div style='margin-bottom:1rem;'>
            <span class='page-title'>Stock Market&nbsp;</span><span class='page-title-accent'>Anomaly Radar</span>
            <p class='page-subtitle' style='margin-top:0.2rem;'>
                Detect unusual price &amp; volume behaviour using
                <strong style='color:#1c2128;font-weight:600;'>Z-Score</strong> and
                <strong style='color:#1c2128;font-weight:600;'>Isolation Forest</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_company_header(info: dict, ticker: str, summary: dict) -> None:
    """
    Render company name, ticker badge, metadata row, and KPI cards.

    Parameters
    ----------
    info : dict
        Keys: name, sector, exchange, currency.
    ticker : str
        Upper-cased ticker symbol e.g. "AAPL".
    summary : dict
        Keys: total_days, total_anomalies, anomaly_rate,
              zscore_only, iforest_only, both_methods, worst_return.
    """
    _render_company_name(info, ticker)
    st.markdown("<hr style='margin:0.75rem 0'/>", unsafe_allow_html=True)
    _render_kpi_cards(summary)
    st.markdown("<hr style='margin:1rem 0'/>", unsafe_allow_html=True)


# ── Private helpers ───────────────────────────────────────────────────────────

def _render_company_name(info: dict, ticker: str) -> None:
    """Company name + ticker badge + sector / exchange / currency row."""
    st.markdown(
        f"""
        <div>
            <div class='company-name'>
                {info['name']}
                <span class='ticker-badge'>{ticker}</span>
            </div>
            <div class='company-meta'>
                <span>{info['sector']}</span>
                <span class='meta-sep'>·</span>
                <span>{info['exchange']}</span>
                <span class='meta-sep'>·</span>
                <span>{info['currency']}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_kpi_cards(summary: dict) -> None:
    """Six compact metric cards in a single row."""
    st.markdown(
        "<p class='section-label'>Summary</p>",
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    c1.metric("Trading Days",    summary["total_days"])
    c2.metric(
        "Total Anomalies",
        summary["total_anomalies"],
        delta=f"{summary['anomaly_rate']}% of days",
        delta_color="off",
    )
    c3.metric("Z-Score Only",  summary["zscore_only"])
    c4.metric("IForest Only",  summary["iforest_only"])
    c5.metric("Both Methods",  summary["both_methods"])
    c6.metric(
        "Worst Return",
        f"{summary['worst_return']}%",
        delta_color="inverse",
    )