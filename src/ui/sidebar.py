"""
src/ui/sidebar.py
-----------------
Collapsible sidebar — hidden by default, slides in on toggle.
Includes comparison mode toggle for side-by-side ticker analysis.
"""

import streamlit as st
from datetime import date, timedelta

_QUICK_TICKERS = ["AAPL", "TSLA", "NVDA", "MSFT", "BTC-USD", "SPY"]


def render_sidebar() -> dict:
    """
    Render the full sidebar and return a config dict.

    Returns
    -------
    dict
        Keys: ticker, ticker_b, compare, start, end,
              zscore_threshold, contamination, run.
    """
    with st.sidebar:
        _render_brand()
        st.markdown("<hr style='margin:0.75rem 0'/>", unsafe_allow_html=True)

        ticker                    = _render_ticker_section("A", "AAPL", "sb_a")
        compare, ticker_b         = _render_comparison_section()
        st.markdown("<hr style='margin:0.75rem 0'/>", unsafe_allow_html=True)

        start_date, end_date      = _render_date_section()
        st.markdown("<hr style='margin:0.75rem 0'/>", unsafe_allow_html=True)

        zscore_threshold, contamination = _render_detector_section()
        st.markdown("<hr style='margin:0.75rem 0'/>", unsafe_allow_html=True)

        run = st.button("▶  Run Analysis", use_container_width=True, type="primary")

        _render_footer()

    return {
        "ticker":           ticker,
        "ticker_b":         ticker_b,
        "compare":          compare,
        "start":            str(start_date),
        "end":              str(end_date),
        "zscore_threshold": float(zscore_threshold),
        "contamination":    float(contamination),
        "run":              run,
    }


# ── Private helpers ───────────────────────────────────────────────────────────

def _render_brand() -> None:
    st.markdown(
        """
        <div style='margin-bottom:0.25rem;'>
            <div style='font-family:"Plus Jakarta Sans",sans-serif;
                        font-size:0.95rem;font-weight:700;
                        color:#fff;letter-spacing:-0.02em;'>
                Anomaly Radar
            </div>
            <div style='font-family:"JetBrains Mono",monospace;
                        font-size:0.6rem;color:#52525b;
                        margin-top:0.1rem;letter-spacing:0.08em;'>
                Z-SCORE · ISOLATION FOREST
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_ticker_section(label: str, default: str, key_prefix: str) -> str:
    """
    Ticker text input + quick-pick chips.
    Reads st.session_state["selected_ticker"] if set (from clicking
    a suggested ticker on the empty state page).

    Parameters
    ----------
    label       : "A" for primary, "B" for comparison ticker
    default     : default ticker value
    key_prefix  : unique key prefix to avoid Streamlit widget key collisions
    """
    st.markdown(
        f"<div class='sidebar-section'>Ticker {label}</div>",
        unsafe_allow_html=True,
    )

    # ── Transfer any pending value BEFORE the widget renders ────────────
    # Streamlit forbids writing to a widget key after it's instantiated.
    # So we use a separate "pending" key as a one-rerun buffer:
    #   click → write to pending → rerun → transfer to widget key → render
    pending_key  = f"{key_prefix}_pending"
    widget_key   = f"{key_prefix}_input"

    # Source 1: quick-pick button clicked in sidebar
    if st.session_state.get(pending_key):
        st.session_state[widget_key] = st.session_state.pop(pending_key)

    # Source 2: quick-start row clicked on empty state page
    if label == "A" and st.session_state.get("selected_ticker"):
        st.session_state[widget_key] = st.session_state.pop("selected_ticker")

    # ── Widget renders here — reads from session state ────────────────
    ticker = st.text_input(
        f"Ticker {label}",
        value=default,
        max_chars=10,
        label_visibility="collapsed",
        placeholder="e.g. AAPL, TSLA, BTC-USD",
        key=widget_key,
    ).upper().strip()

    # ── Quick-pick buttons ────────────────────────────────────────────
    current = st.session_state.get(widget_key, default).upper().strip()

    row1 = st.columns(3)
    row2 = st.columns(3)
    for col, qt in zip(row1 + row2, _QUICK_TICKERS):
        is_active = current == qt.upper()
        if col.button(
            qt,
            use_container_width=True,
            key=f"{key_prefix}_{qt}",
            type="primary" if is_active else "secondary",
        ):
            # Write to pending — picked up on the next rerun before widget renders
            st.session_state[pending_key] = qt
            st.rerun()

    return ticker


def _render_comparison_section() -> tuple[bool, str]:
    """
    Comparison mode toggle. When enabled, shows a second ticker input.

    Returns
    -------
    tuple[bool, str]
        (compare_enabled, ticker_b)
    """
    st.markdown(
        "<div class='sidebar-section'>Comparison Mode</div>",
        unsafe_allow_html=True,
    )

    compare = st.toggle(
        "Compare two tickers side by side",
        value=False,
        key="compare_toggle",
        help="Run anomaly detection on two tickers and view charts side by side.",
    )

    ticker_b = ""
    if compare:
        ticker_b = _render_ticker_section("B", "MSFT", "sb_b")

    return compare, ticker_b


def _render_date_section() -> tuple[date, date]:
    """Start / end date inputs side by side."""
    st.markdown("<div class='sidebar-section'>Date Range</div>", unsafe_allow_html=True)

    default_end   = date.today()
    default_start = default_end - timedelta(days=365 * 2)

    col_s, col_e = st.columns(2)
    with col_s:
        start_date = st.date_input(
            "From", value=default_start,
            max_value=default_end,
            label_visibility="collapsed",
        )
    with col_e:
        end_date = st.date_input(
            "To", value=default_end,
            max_value=default_end,
            label_visibility="collapsed",
        )

    return start_date, end_date


def _render_detector_section() -> tuple[float, float]:
    """Z-Score threshold and IF contamination sliders."""
    st.markdown("<div class='sidebar-section'>Detection</div>", unsafe_allow_html=True)

    st.caption("Z-Score Threshold")
    zscore_threshold = st.slider(
        "Z-Score", min_value=1.5, max_value=5.0,
        value=2.5, step=0.1,
        label_visibility="collapsed",
        help="Days whose |Z-score| exceeds this are flagged. Lower = more sensitive.",
    )

    st.caption("IF Contamination")
    contamination = st.slider(
        "Contamination", min_value=0.01, max_value=0.20,
        value=0.05, step=0.01, format="%.2f",
        label_visibility="collapsed",
        help="Expected proportion of anomalies (0.01–0.20).",
    )

    return zscore_threshold, contamination


def _render_footer() -> None:
    st.markdown(
        """
        <div style='margin-top:2rem;padding-top:1rem;
                    border-top:1px solid rgba(255,255,255,0.07);'>
            <div style='font-family:"JetBrains Mono",monospace;
                        font-size:0.6rem;color:#52525b;line-height:1.9;'>
                Data via yfinance<br>
                scikit-learn IForest<br>
                Plotly · Streamlit
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )