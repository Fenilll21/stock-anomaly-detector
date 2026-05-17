"""
src/ui/header.py
----------------
Page-level and results-level header components for the Stock Market
Anomaly Detector.

Functions
---------
render_page_header()
    Renders the app title and subtitle shown at the top of every page load.
    Call once, right after inject_styles().

render_company_header(info, ticker, summary)
    Renders the company name, ticker badge, sector metadata, a divider,
    and the six KPI metric cards.
    Call only when results are available.

Usage
-----
    from src.ui.header import render_page_header, render_company_header

    render_page_header()

    if st.session_state["results"]:
        res = st.session_state["results"]
        render_company_header(res["info"], res["ticker"], res["summary"])
"""

import streamlit as st


def render_page_header() -> None:
    """
    Render the main app title and one-line description.

    Displays a two-tone display heading (white + accent) and a short
    subtitle explaining the two detection methods. Should be called once
    at the top of the main content area, after inject_styles().
    """
    st.markdown(
        """
        <div style='margin-bottom:0.25rem'>
            <span style='font-family:var(--font-display,sans-serif);font-size:1.9rem;
                         font-weight:800;color:#f0f6ff;letter-spacing:-0.02em;'>
                Stock Market
            </span>
            <span style='font-family:var(--font-display,sans-serif);font-size:1.9rem;
                         font-weight:800;color:#38bdf8;letter-spacing:-0.02em;'>
                Anomaly Radar
            </span>
        </div>
        <p style='font-family:"DM Sans",sans-serif;font-size:0.88rem;
                  color:#8da3be;margin-top:0.25rem;'>
            Detect unusual price &amp; volume behaviour using
            <strong style='color:#f0f6ff;font-weight:500;'>Z-Score</strong> and
            <strong style='color:#f0f6ff;font-weight:500;'>Isolation Forest</strong>.
            Configure parameters in the sidebar, then hit <em>Run Analysis</em>.
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<hr style='margin:1rem 0 1.5rem'/>", unsafe_allow_html=True)


def render_company_header(info: dict, ticker: str, summary: dict) -> None:
    """
    Render the company name, ticker badge, metadata row, and KPI cards.

    Parameters
    ----------
    info : dict
        Ticker info returned by get_ticker_info(). Expected keys:
        ``name``, ``sector``, ``exchange``, ``currency``.
    ticker : str
        Upper-cased ticker symbol, e.g. ``"AAPL"``.
    summary : dict
        Anomaly summary returned by get_anomaly_summary(). Expected keys:
        ``total_days``, ``total_anomalies``, ``anomaly_rate``,
        ``zscore_only``, ``iforest_only``, ``both_methods``, ``worst_return``.
    """
    _render_company_name(info, ticker)
    st.markdown("<hr style='margin:1rem 0 1.25rem'/>", unsafe_allow_html=True)
    _render_kpi_cards(summary)
    st.markdown("<hr style='margin:1.5rem 0 1.25rem'/>", unsafe_allow_html=True)


# ── Private helpers ───────────────────────────────────────────────────────────

def _render_company_name(info: dict, ticker: str) -> None:
    """Company name + ticker badge + sector / exchange / currency metadata."""
    st.markdown(
        f"""
        <div class='company-header'>
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
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_kpi_cards(summary: dict) -> None:
    """Six metric cards displayed in a single row."""
    st.markdown("<p class='section-label'>Overview</p>", unsafe_allow_html=True)

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    c1.metric(
        "Trading Days",
        summary["total_days"],
    )
    c2.metric(
        "Total Anomalies",
        summary["total_anomalies"],
        delta=f"{summary['anomaly_rate']}% of days",
        delta_color="off",
    )
    c3.metric(
        "Z-Score Only",
        summary["zscore_only"],
    )
    c4.metric(
        "IForest Only",
        summary["iforest_only"],
    )
    c5.metric(
        "Both Methods",
        summary["both_methods"],
    )
    c6.metric(
        "Worst Return",
        f"{summary['worst_return']}%",
        delta_color="inverse",
    )