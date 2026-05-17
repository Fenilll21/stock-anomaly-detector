"""
src/ui/sidebar.py
-----------------
Sidebar panel for the Stock Market Anomaly Detector.

Renders all user-configurable controls and returns a single config dict
so that app.py never has to touch st.sidebar directly.

Usage
-----
    from src.ui.sidebar import render_sidebar

    config = render_sidebar()

    if config["run"]:
        df = fetch_stock_data(config["ticker"], config["start"], config["end"])
        df = run_anomaly_detection(df, config["zscore_threshold"], config["contamination"])

Returned config keys
--------------------
    ticker            str   – upper-cased ticker symbol, e.g. "AAPL"
    start             str   – ISO date string, e.g. "2023-01-01"
    end               str   – ISO date string, e.g. "2025-01-01"
    zscore_threshold  float – Z-score anomaly threshold (1.5 – 5.0)
    contamination     float – Isolation Forest contamination (0.01 – 0.20)
    run               bool  – True when the user clicked "Run Analysis"
"""

import streamlit as st
from datetime import date, timedelta


# Tickers shown as quick-pick buttons below the text input
_QUICK_TICKERS = ["AAPL", "TSLA", "NVDA", "MSFT"]


def render_sidebar() -> dict:
    """
    Render the full sidebar and return a config dict with all user choices.

    Returns
    -------
    dict
        Keys: ticker, start, end, zscore_threshold, contamination, run.
    """
    with st.sidebar:
        _render_brand()
        st.markdown("---")

        ticker = _render_ticker_section()
        st.markdown("---")

        start_date, end_date = _render_date_section()
        st.markdown("---")

        zscore_threshold, contamination = _render_detector_section()
        st.markdown("---")

        run = _render_run_button()
        st.markdown("---")

        _render_footer()

    return {
        "ticker":           ticker,
        "start":            str(start_date),
        "end":              str(end_date),
        "zscore_threshold": zscore_threshold,
        "contamination":    contamination,
        "run":              run,
    }


# ── Private helpers ───────────────────────────────────────────────────────────

def _render_brand() -> None:
    """App name + live status pill."""
    st.markdown(
        "<h1 style='margin-bottom:0'>📡 Anomaly Radar</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<span class='status-pill'>LIVE</span>",
        unsafe_allow_html=True,
    )


def _render_ticker_section() -> str:
    """
    Ticker text input + quick-pick buttons.

    Returns
    -------
    str
        Upper-cased ticker symbol chosen by the user.
    """
    st.subheader("Stock Selection")

    ticker = st.text_input(
        "Ticker Symbol",
        value="AAPL",
        max_chars=10,
        label_visibility="collapsed",
        placeholder="e.g. TSLA, NVDA, BTC-USD",
        help="Enter any valid Yahoo Finance ticker symbol.",
    ).upper().strip()

    st.caption("QUICK PICKS")
    cols = st.columns(len(_QUICK_TICKERS))
    for col, qt in zip(cols, _QUICK_TICKERS):
        if col.button(qt, use_container_width=True):
            ticker = qt

    return ticker


def _render_date_section() -> tuple[date, date]:
    """
    Start / end date inputs rendered side-by-side.

    Returns
    -------
    tuple[date, date]
        (start_date, end_date)
    """
    st.subheader("Date Range")

    default_end   = date.today()
    default_start = default_end - timedelta(days=365 * 2)   # 2-year default

    col_s, col_e = st.columns(2)
    with col_s:
        start_date = st.date_input("From", value=default_start, max_value=default_end)
    with col_e:
        end_date = st.date_input("To", value=default_end, max_value=default_end)

    return start_date, end_date


def _render_detector_section() -> tuple[float, float]:
    """
    Z-Score threshold and Isolation Forest contamination sliders.

    Returns
    -------
    tuple[float, float]
        (zscore_threshold, contamination)
    """
    st.subheader("Detector Settings")

    st.caption("Z-SCORE THRESHOLD")
    zscore_threshold = st.slider(
        "Z-Score Threshold",
        min_value=1.5,
        max_value=5.0,
        value=2.5,
        step=0.1,
        label_visibility="collapsed",
        help=(
            "Days whose |Z-score| exceeds this value are flagged. "
            "Lower = more sensitive (more anomalies flagged)."
        ),
    )

    st.caption("ISOLATION FOREST CONTAMINATION")
    contamination = st.slider(
        "IF Contamination",
        min_value=0.01,
        max_value=0.20,
        value=0.05,
        step=0.01,
        format="%.2f",
        label_visibility="collapsed",
        help=(
            "Expected proportion of anomalies (0.01–0.20). "
            "Higher = Isolation Forest flags more points as anomalous."
        ),
    )

    return zscore_threshold, contamination


def _render_run_button() -> bool:
    """
    Primary action button.

    Returns
    -------
    bool
        True if the button was clicked this run.
    """
    return st.button(
        "▶  RUN ANALYSIS",
        use_container_width=True,
        type="primary",
    )


def _render_footer() -> None:
    """Small attribution caption at the bottom of the sidebar."""
    st.caption(
        "Z-Score · Isolation Forest  \n"
        "Data via [yfinance](https://github.com/ranaroussi/yfinance)"
    )