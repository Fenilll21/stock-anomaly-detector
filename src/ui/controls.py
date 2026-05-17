"""
src/ui/controls.py
------------------
Inline horizontal control bar for the Stock Market Anomaly Detector.

Replaces the sidebar entirely. All user-configurable parameters are
rendered in a compact card at the top of the main content area so
the full viewport width is available for charts.

Usage
-----
    from src.ui.controls import render_controls

    config = render_controls()

    if config["run"]:
        df = fetch_stock_data(config["ticker"], config["start"], config["end"])

Returned config keys
--------------------
    ticker            str   – upper-cased ticker symbol, e.g. "AAPL"
    start             str   – ISO date string, e.g. "2023-01-01"
    end               str   – ISO date string, e.g. "2025-05-17"
    zscore_threshold  float – Z-score anomaly threshold (1.5 – 5.0)
    contamination     float – Isolation Forest contamination (0.01 – 0.20)
    run               bool  – True when the user clicked Run Analysis
"""

import streamlit as st
from datetime import date, timedelta

_QUICK_TICKERS = ["AAPL", "TSLA", "NVDA", "MSFT", "BTC-USD", "SPY"]

_DEFAULT_ZSCORE        = 2.5
_DEFAULT_CONTAMINATION = 0.05


def render_controls() -> dict:
    """
    Render the compact inline control bar and return a config dict.

    Layout (two rows inside a surface card):
        Row 1 — Ticker input · quick-pick chips · date range · Run button
        Row 2 — Z-Score threshold · Contamination (number inputs + labels)

    Returns
    -------
    dict
        Keys: ticker, start, end, zscore_threshold, contamination, run.
    """
    st.markdown("<div class='control-bar'>", unsafe_allow_html=True)
    st.markdown(
        "<p class='control-bar-title'>⚙ Configuration</p>",
        unsafe_allow_html=True,
    )

    ticker, start_date, end_date, run = _render_row_one()
    zscore_threshold, contamination   = _render_row_two()

    st.markdown("</div>", unsafe_allow_html=True)

    return {
        "ticker":           ticker,
        "start":            str(start_date),
        "end":              str(end_date),
        "zscore_threshold": zscore_threshold,
        "contamination":    contamination,
        "run":              run,
    }


# ── Private helpers ───────────────────────────────────────────────────────────

def _render_row_one() -> tuple:
    """
    Row 1: ticker input | quick picks | date from | date to | run button.

    Returns
    -------
    tuple
        (ticker: str, start_date: date, end_date: date, run: bool)
    """
    # Column widths: ticker | 6 quick picks | date from | date to | run btn
    c_ticker, c_q1, c_q2, c_q3, c_q4, c_q5, c_q6, c_from, c_to, c_run = st.columns(
        [2, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 1.6, 1.6, 1.4]
    )

    with c_ticker:
        ticker = st.text_input(
            "Ticker",
            value="AAPL",
            max_chars=10,
            label_visibility="collapsed",
            placeholder="Ticker — e.g. AAPL",
            help="Any valid Yahoo Finance ticker.",
        ).upper().strip()

    # Quick-pick chips
    quick_cols = [c_q1, c_q2, c_q3, c_q4, c_q5, c_q6]
    for col, qt in zip(quick_cols, _QUICK_TICKERS):
        if col.button(qt, use_container_width=True, key=f"qp_{qt}"):
            ticker = qt

    default_end   = date.today()
    default_start = default_end - timedelta(days=365 * 2)

    with c_from:
        start_date = st.date_input(
            "From",
            value=default_start,
            max_value=default_end,
            label_visibility="collapsed",
            help="Analysis start date.",
        )

    with c_to:
        end_date = st.date_input(
            "To",
            value=default_end,
            max_value=default_end,
            label_visibility="collapsed",
            help="Analysis end date.",
        )

    with c_run:
        run = st.button(
            "▶  Run Analysis",
            use_container_width=True,
            type="primary",
        )

    return ticker, start_date, end_date, run


def _render_row_two() -> tuple:
    """
    Row 2: Z-Score threshold and Isolation Forest contamination inputs.
    Uses number_input for compactness — no tall slider track needed.

    Returns
    -------
    tuple
        (zscore_threshold: float, contamination: float)
    """
    st.markdown(
        "<div style='margin-top:0.6rem;border-top:1px solid var(--border);"
        "padding-top:0.6rem;'></div>",
        unsafe_allow_html=True,
    )

    c_zl, c_zv, c_gap, c_cl, c_cv, c_rest = st.columns([1.5, 1, 0.3, 1.8, 1, 5.4])

    with c_zl:
        st.markdown(
            "<p style='font-family:var(--font-mono,monospace);font-size:0.72rem;"
            "color:var(--text-muted);margin:0;padding-top:0.45rem;'>"
            "Z-Score threshold</p>",
            unsafe_allow_html=True,
        )

    with c_zv:
        zscore_threshold = st.number_input(
            "Z-Score",
            min_value=1.5,
            max_value=5.0,
            value=_DEFAULT_ZSCORE,
            step=0.1,
            format="%.1f",
            label_visibility="collapsed",
            help="Days whose |Z-score| exceeds this are flagged. Lower = more sensitive.",
            key="zscore_input",
        )

    with c_cl:
        st.markdown(
            "<p style='font-family:var(--font-mono,monospace);font-size:0.72rem;"
            "color:var(--text-muted);margin:0;padding-top:0.45rem;'>"
            "IF contamination</p>",
            unsafe_allow_html=True,
        )

    with c_cv:
        contamination = st.number_input(
            "Contamination",
            min_value=0.01,
            max_value=0.20,
            value=_DEFAULT_CONTAMINATION,
            step=0.01,
            format="%.2f",
            label_visibility="collapsed",
            help="Expected proportion of anomalies (0.01–0.20). Higher = more flagged.",
            key="contamination_input",
        )

    return float(zscore_threshold), float(contamination)