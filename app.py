"""
app.py  —  Stock Market Anomaly Radar
Pipeline runs FIRST, then header renders — so live banner and home
button always see the correct session state on first run.
"""

import streamlit as st
import streamlit.components.v1 as components

from src.data_fetcher     import fetch_stock_data, get_ticker_info, validate_date_range
from src.anomaly_detector import run_anomaly_detection, get_anomaly_summary
from src.ui               import (
    inject_styles,
    render_sidebar,
    render_page_header,
    render_live_price_banner,
    render_company_header,
    render_chart_tabs,
    render_anomaly_table,
    render_anomaly_timeline,
    render_empty_state,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Anomaly Radar",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Styles ────────────────────────────────────────────────────────────────────
inject_styles()

# ── Session-state init ────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state["results"] = None
if "error" not in st.session_state:
    st.session_state["error"]   = None
if "reset_sidebar" not in st.session_state:
    st.session_state["reset_sidebar"] = False

# ── Sidebar scroll reset ──────────────────────────────────────────────────────
# When home button is clicked we set reset_sidebar=True before rerun.
# On this rerun we inject JS to scroll the sidebar back to the top,
# then clear the flag so it only fires once.
if st.session_state.pop("reset_sidebar", False):
    components.html(
        """
        <script>
        (function() {
            // Scroll sidebar inner div to top smoothly
            const sel = '[data-testid="stSidebar"] > div:first-child';
            const sidebar = window.parent.document.querySelector(sel);
            if (sidebar) sidebar.scrollTo({ top: 0, behavior: "smooth" });
        })();
        </script>
        """,
        height=0,
    )

# ── Sidebar → config ──────────────────────────────────────────────────────────
# Sidebar renders here but we run the pipeline before the main content
config   = render_sidebar()
ticker_a = config["ticker"]
ticker_b = config["ticker_b"] if config["compare"] else ""

# ── Run pipeline FIRST ────────────────────────────────────────────────────────
# This must happen before render_page_header() so that session state
# is populated when the home button + live banner check it
if config["run"]:
    st.session_state["results"] = None
    st.session_state["error"]   = None

    try:
        validate_date_range(config["start"], config["end"])

        with st.spinner(f"Fetching {ticker_a}…"):
            df   = fetch_stock_data(ticker_a, config["start"], config["end"])
            info = get_ticker_info(ticker_a)

        if config["compare"] and ticker_b:
            with st.spinner(f"Fetching {ticker_b}…"):
                df_b   = fetch_stock_data(ticker_b, config["start"], config["end"])
                info_b = get_ticker_info(ticker_b)
        else:
            df_b, info_b = None, None

        with st.spinner("Running anomaly detection…"):
            df      = run_anomaly_detection(df, config["zscore_threshold"], config["contamination"])
            summary = get_anomaly_summary(df)

            if df_b is not None:
                df_b      = run_anomaly_detection(df_b, config["zscore_threshold"], config["contamination"])
                summary_b = get_anomaly_summary(df_b)
            else:
                summary_b = None

        st.session_state["results"] = {
            "df": df, "info": info, "summary": summary, "ticker": ticker_a,
            "df_b": df_b, "info_b": info_b, "summary_b": summary_b,
            "ticker_b": ticker_b, "compare": config["compare"],
        }

    except ValueError as ve:
        st.session_state["error"] = str(ve)
    except Exception as ex:
        st.session_state["error"] = f"Unexpected error: {ex}"

# ── NOW render page header + live banner ──────────────────────────────────────
# Session state is fully populated at this point — home button and
# live banner will correctly reflect the current state
render_page_header()
render_live_price_banner(ticker_a, ticker_b)

st.markdown("<hr style='margin:0.5rem 0 1.25rem'/>", unsafe_allow_html=True)

# ── Error banner ──────────────────────────────────────────────────────────────
if st.session_state["error"]:
    st.error(f"⚠ {st.session_state['error']}", icon="🚨")

# ── Results or empty state ────────────────────────────────────────────────────
if st.session_state["results"]:
    res     = st.session_state["results"]
    compare = res["compare"]

    if compare and res["df_b"] is not None:
        col_a, col_b = st.columns(2)
        with col_a:
            render_company_header(res["info"],   res["ticker"],   res["summary"])
            render_anomaly_timeline(res["df"])
            render_chart_tabs(res["df"],   res["ticker"])
            render_anomaly_table(res["df"],   res["ticker"])
        with col_b:
            render_company_header(res["info_b"], res["ticker_b"], res["summary_b"])
            render_anomaly_timeline(res["df_b"])
            render_chart_tabs(res["df_b"], res["ticker_b"])
            render_anomaly_table(res["df_b"], res["ticker_b"])
    else:
        render_company_header(res["info"], res["ticker"], res["summary"])
        render_anomaly_timeline(res["df"])
        render_chart_tabs(res["df"], res["ticker"])
        render_anomaly_table(res["df"], res["ticker"])

else:
    if not st.session_state["error"]:
        render_empty_state()