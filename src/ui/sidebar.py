"""
src/ui/sidebar.py
-----------------
Collapsible sidebar — hidden by default, slides in on toggle.
Clean dark controls with minimal chrome.
"""

import streamlit as st
from datetime import date, timedelta

_QUICK_TICKERS = ["AAPL", "TSLA", "NVDA", "MSFT", "BTC-USD", "SPY"]


def render_sidebar() -> dict:
    with st.sidebar:
        # ── Brand ─────────────────────────────────────────────────────
        st.markdown(
            """
            <div style='margin-bottom:1.25rem;'>
                <div style='font-family:"Plus Jakarta Sans",sans-serif;
                            font-size:0.95rem;font-weight:700;
                            color:#fff;letter-spacing:-0.02em;'>
                    Anomaly Radar
                </div>
                <div style='font-family:"JetBrains Mono",monospace;
                            font-size:0.62rem;color:#52525b;
                            margin-top:0.15rem;letter-spacing:0.06em;'>
                    Z-SCORE · ISOLATION FOREST
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div class='sidebar-section'>Ticker</div>", unsafe_allow_html=True)

        ticker = st.text_input(
            "Ticker",
            value="AAPL",
            max_chars=10,
            label_visibility="collapsed",
            placeholder="e.g. AAPL, TSLA, BTC-USD",
        ).upper().strip()

        # Quick picks — 3 per row
        row1 = st.columns(3)
        row2 = st.columns(3)
        all_cols = row1 + row2
        for col, qt in zip(all_cols, _QUICK_TICKERS):
            if col.button(qt, use_container_width=True, key=f"sb_{qt}"):
                ticker = qt

        # ── Date range ────────────────────────────────────────────────
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

        # ── Detector settings ─────────────────────────────────────────
        st.markdown("<div class='sidebar-section'>Detection</div>", unsafe_allow_html=True)

        st.caption("Z-Score Threshold")
        zscore_threshold = st.slider(
            "Z-Score", min_value=1.5, max_value=5.0,
            value=2.5, step=0.1,
            label_visibility="collapsed",
            help="Days whose |Z-score| exceeds this are flagged.",
        )

        st.caption("IF Contamination")
        contamination = st.slider(
            "Contamination", min_value=0.01, max_value=0.20,
            value=0.05, step=0.01, format="%.2f",
            label_visibility="collapsed",
            help="Expected proportion of anomalies (0.01–0.20).",
        )

        # ── Run ───────────────────────────────────────────────────────
        st.markdown("<div class='sidebar-section'></div>", unsafe_allow_html=True)
        run = st.button(
            "▶  Run Analysis",
            use_container_width=True,
            type="primary",
        )

        # ── Footer ────────────────────────────────────────────────────
        st.markdown(
            """
            <div style='margin-top:2rem;padding-top:1rem;
                        border-top:1px solid rgba(255,255,255,0.07);'>
                <div style='font-family:"JetBrains Mono",monospace;
                            font-size:0.6rem;color:#52525b;line-height:1.8;'>
                    Data via yfinance<br>
                    scikit-learn IForest<br>
                    Plotly · Streamlit
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return {
        "ticker":           ticker,
        "start":            str(start_date),
        "end":              str(end_date),
        "zscore_threshold": float(zscore_threshold),
        "contamination":    float(contamination),
        "run":              run,
    }