"""
app.py  —  Stock Market Anomaly Radar
Sidebar hidden by default, slides in on toggle.
"""

import streamlit as st

from src.data_fetcher     import fetch_stock_data, get_ticker_info, validate_date_range
from src.anomaly_detector import run_anomaly_detection, get_anomaly_summary
from src.ui               import (
    inject_styles, render_sidebar,
    render_page_header, render_company_header,
    render_chart_tabs, render_anomaly_table, render_empty_state,
)

st.set_page_config(
    page_title="Anomaly Radar",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_page_header()

config = render_sidebar()

st.markdown("<hr style='margin:0.5rem 0 1.25rem'/>", unsafe_allow_html=True)

if "results" not in st.session_state:
    st.session_state["results"] = None
if "error" not in st.session_state:
    st.session_state["error"]   = None

if config["run"]:
    st.session_state["results"] = None
    st.session_state["error"]   = None
    try:
        validate_date_range(config["start"], config["end"])
        with st.spinner(f"Fetching {config['ticker']}…"):
            df   = fetch_stock_data(config["ticker"], config["start"], config["end"])
            info = get_ticker_info(config["ticker"])
        with st.spinner("Running anomaly detection…"):
            df      = run_anomaly_detection(df, config["zscore_threshold"], config["contamination"])
            summary = get_anomaly_summary(df)
        st.session_state["results"] = {"df": df, "info": info,
                                        "summary": summary, "ticker": config["ticker"]}
    except ValueError as ve:
        st.session_state["error"] = str(ve)
    except Exception as ex:
        st.session_state["error"] = f"Unexpected error: {ex}"

if st.session_state["error"]:
    st.error(f"⚠ {st.session_state['error']}", icon="🚨")

if st.session_state["results"]:
    res = st.session_state["results"]
    render_company_header(res["info"], res["ticker"], res["summary"])
    render_chart_tabs(res["df"], res["ticker"])
    render_anomaly_table(res["df"], res["ticker"])
else:
    if not st.session_state["error"]:
        render_empty_state()