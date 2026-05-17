"""
src/ui/charts.py
----------------
Chart tabs, anomaly timeline, anomaly detail modal,
raw data table, and empty state.

New in this version
-------------------
- 6th tab: Anomaly Calendar heatmap
- Anomaly timeline: horizontal scrollable event strip
- Anomaly detail modal: @st.dialog popup on row click
- render_empty_state: suggested tickers table
"""

import pandas as pd
import streamlit as st

from src.visualizer import (
    plot_price_anomalies,
    plot_zscore_heatmap,
    plot_iforest_scores,
    plot_return_distribution,
    plot_anomaly_scatter,
    plot_calendar_heatmap,
)

_ANOMALY_COLUMNS = [
    "Open", "High", "Low", "Close", "Volume",
    "Daily_Return", "Price_Range",
    "ZScore_Anomaly", "IForest_Anomaly", "Anomaly_Type",
]
_COLUMN_FORMATS = {
    "Open": "${:.2f}", "High": "${:.2f}",
    "Low":  "${:.2f}", "Close": "${:.2f}",
    "Volume": "{:,.0f}",
    "Daily_Return": "{:.2f}%",
    "Price_Range":  "{:.2f}%",
}
_EXAMPLE_TICKERS = {
    "Ticker": ["AAPL", "TSLA", "NVDA", "BTC-USD", "SPY",  "AMZN"],
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

# Anomaly type → badge colour
_TYPE_COLOURS = {
    "Z-Score Only":          ("#f59e0b", "#1a1400"),
    "Isolation Forest Only": ("#8b5cf6", "#120d1f"),
    "Both Methods":          ("#ef4444", "#1f0a0a"),
}


# ── Modal ─────────────────────────────────────────────────────────────────────

@st.dialog("Anomaly Detail")
def _show_anomaly_modal(row: pd.Series, date_str: str) -> None:
    """
    Dark popup modal showing full detail for a single anomaly day.
    Triggered by clicking a date button in the anomaly timeline or table.
    """
    atype   = row.get("Anomaly_Type", "Unknown")
    colours = _TYPE_COLOURS.get(atype, ("#a1a1aa", "#1a1a1a"))
    accent, bg = colours

    st.markdown(
        f"""
        <div style='margin-bottom:1rem;'>
            <div style='font-family:"JetBrains Mono",monospace;
                        font-size:0.65rem;color:#52525b;
                        letter-spacing:0.1em;margin-bottom:0.3rem;'>
                ANOMALY DETECTED
            </div>
            <div style='font-family:"Plus Jakarta Sans",sans-serif;
                        font-size:1.1rem;font-weight:700;
                        color:#fff;letter-spacing:-0.02em;'>
                {date_str}
            </div>
            <span style='display:inline-block;margin-top:0.4rem;
                         background:{bg};border:1px solid {accent};
                         border-radius:4px;color:{accent};
                         font-family:"JetBrains Mono",monospace;
                         font-size:0.7rem;font-weight:500;
                         padding:0.15rem 0.5rem;letter-spacing:0.04em;'>
                {atype}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Price metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Open",  f"${row['Open']:.2f}")
    c2.metric("High",  f"${row['High']:.2f}")
    c3.metric("Low",   f"${row['Low']:.2f}")
    c4.metric("Close", f"${row['Close']:.2f}")

    st.markdown("<hr style='margin:0.75rem 0'/>", unsafe_allow_html=True)

    # Return + volume
    c5, c6 = st.columns(2)
    ret = row["Daily_Return"]
    ret_colour = "#22c55e" if ret >= 0 else "#ef4444"
    c5.metric("Daily Return", f"{ret:.2f}%")
    c6.metric("Volume",       f"{row['Volume']:,.0f}")

    st.markdown("<hr style='margin:0.75rem 0'/>", unsafe_allow_html=True)

    # Detection flags
    st.markdown("<p class='section-label'>Detection flags</p>", unsafe_allow_html=True)
    fc1, fc2 = st.columns(2)
    fc1.metric("Z-Score Flag",   "✓ Yes" if row.get("ZScore_Anomaly")  else "✗ No")
    fc2.metric("IForest Flag",   "✓ Yes" if row.get("IForest_Anomaly") else "✗ No")

    if "Price_Range" in row:
        st.markdown("<hr style='margin:0.75rem 0'/>", unsafe_allow_html=True)
        st.metric("Price Range", f"{row['Price_Range']:.2f}%",
                  help="(High - Low) / Open × 100")


# ── Public API ────────────────────────────────────────────────────────────────

def render_anomaly_timeline(df: pd.DataFrame, key_prefix: str = "a") -> None:
    """
    Horizontal scrollable event strip showing the most recent anomalies.
    Each card is clickable and opens the detail modal.

    Parameters
    ----------
    df         : pd.DataFrame — must contain Is_Anomaly, Anomaly_Type, Daily_Return
    key_prefix : str — unique prefix per call to avoid duplicate widget keys
                       use "a" for primary ticker, "b" for comparison ticker
    """
    anomalies = (
        df[df["Is_Anomaly"]]
        .sort_index(ascending=False)
        .head(12)                 # show last 12 anomalies max
    )

    if anomalies.empty:
        return

    st.markdown("<p class='section-label'>Recent Anomalies</p>", unsafe_allow_html=True)

    # Build one HTML card per anomaly, all in a flex row with overflow-x scroll
    cards_html = ""
    for date_idx, row in anomalies.iterrows():
        date_str  = pd.Timestamp(date_idx).strftime("%d %b %Y")
        atype     = row.get("Anomaly_Type", "Unknown")
        accent, bg = _TYPE_COLOURS.get(atype, ("#a1a1aa", "#1a1a1a"))
        ret       = row["Daily_Return"]
        ret_sign  = "+" if ret >= 0 else ""
        ret_col   = "#22c55e" if ret >= 0 else "#ef4444"

        cards_html += f"""
        <div style='
            min-width:140px; max-width:140px;
            background:#111111;
            border:1px solid rgba(255,255,255,0.07);
            border-left:3px solid {accent};
            border-radius:8px;
            padding:0.7rem 0.8rem;
            flex-shrink:0;
            cursor:default;
        '>
            <div style='font-family:"JetBrains Mono",monospace;
                        font-size:0.62rem;color:#52525b;
                        margin-bottom:0.35rem;'>{date_str}</div>
            <div style='font-family:"JetBrains Mono",monospace;
                        font-size:0.9rem;font-weight:500;
                        color:{ret_col};margin-bottom:0.4rem;'>
                {ret_sign}{ret:.2f}%
            </div>
            <span style='
                background:{bg};border:1px solid {accent};
                border-radius:3px;color:{accent};
                font-family:"JetBrains Mono",monospace;
                font-size:0.58rem;padding:0.1rem 0.35rem;
                letter-spacing:0.03em;white-space:nowrap;
            '>{atype.replace("Isolation Forest", "IForest")}</span>
        </div>
        """

    st.markdown(
        f"""
        <div style='
            display:flex;gap:0.6rem;
            overflow-x:auto;padding:0.25rem 0 0.75rem;
            scrollbar-width:thin;
            scrollbar-color:#1a1a1a #0a0a0a;
        '>
            {cards_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Clickable date selector for modal
    st.markdown(
        "<p style='font-family:\"JetBrains Mono\",monospace;"
        "font-size:0.62rem;color:#52525b;margin-bottom:0.3rem;'>"
        "Click a date for full detail →</p>",
        unsafe_allow_html=True,
    )

    date_options = [
        pd.Timestamp(d).strftime("%d %b %Y")
        for d in anomalies.index
    ]
    cols = st.columns(min(len(date_options), 6))
    for i, (col, (date_idx, row)) in enumerate(
        zip(cols, anomalies.head(6).iterrows())
    ):
        date_str = pd.Timestamp(date_idx).strftime("%d %b %Y")
        if col.button(date_str, key=f"tl_{key_prefix}_btn_{i}", use_container_width=True):
            _show_anomaly_modal(row, date_str)

    st.markdown("<hr style='margin:0.75rem 0 1.25rem'/>", unsafe_allow_html=True)


def render_chart_tabs(df: pd.DataFrame, ticker: str) -> None:
    """
    Six analysis tabs with Plotly charts.

    Parameters
    ----------
    df     : processed dataframe from run_anomaly_detection()
    ticker : upper-cased symbol e.g. "AAPL"
    """
    st.markdown("<p class='section-label'>Analysis</p>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Price & Volume",
        "Z-Score",
        "Isolation Forest",
        "Return Distribution",
        "Feature Space",
        "📅 Calendar",
    ])

    with tab1:
        _desc("Candlestick with anomaly markers. Red volume bars = anomalous sessions.")
        st.plotly_chart(plot_price_anomalies(df, ticker),
                        use_container_width=True, config=_PLOTLY_CFG)

    with tab2:
        _desc("Absolute Z-scores per feature. Shaded band = anomaly threshold zone.")
        st.plotly_chart(plot_zscore_heatmap(df),
                        use_container_width=True, config=_PLOTLY_CFG)

    with tab3:
        _desc("Isolation Forest scores — higher = more anomalous. Red bars were flagged.")
        st.plotly_chart(plot_iforest_scores(df),
                        use_container_width=True, config=_PLOTLY_CFG)

    with tab4:
        _desc("Daily return distribution: normal vs anomalous. Anomalies cluster in the tails.")
        st.plotly_chart(plot_return_distribution(df),
                        use_container_width=True, config=_PLOTLY_CFG)

    with tab5:
        _desc("Feature space: each dot is a trading day. Colour = detector(s) that flagged it.")
        st.plotly_chart(plot_anomaly_scatter(df),
                        use_container_width=True, config=_PLOTLY_CFG)

    with tab6:
        _desc("Calendar heatmap — anomaly intensity by month and day. "
              "Dark = none · Blue = some · Red = high density.")
        st.plotly_chart(plot_calendar_heatmap(df),
                        use_container_width=True, config=_PLOTLY_CFG)

    st.markdown("<br/>", unsafe_allow_html=True)


def render_anomaly_table(df: pd.DataFrame, ticker: str) -> None:
    """
    Expandable raw anomaly table with CSV download.
    """
    anomaly_df = (
        df[df["Is_Anomaly"]][_ANOMALY_COLUMNS]
        .sort_index(ascending=False)
    )
    n = len(anomaly_df)

    with st.expander(f"🔍  Raw Anomaly Data  ·  {n} records"):
        st.markdown(
            f"<p class='section-label'>{n} anomalous trading days</p>",
            unsafe_allow_html=True,
        )
        st.dataframe(
            anomaly_df.style.format(_COLUMN_FORMATS),
            use_container_width=True,
            height=360,
        )
        col_dl, _ = st.columns([1.5, 8.5])
        with col_dl:
            csv = anomaly_df.reset_index().to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇  Download CSV",
                data=csv,
                file_name=f"{ticker}_anomalies.csv",
                mime="text/csv",
            )


def render_empty_state() -> None:
    """Compact placeholder shown before first analysis run."""

    # Minimal inline prompt — no giant card
    st.markdown(
        """
        <div style='padding:1.25rem 0 1rem;'>
            <span style='font-family:"JetBrains Mono",monospace;
                         font-size:0.78rem;color:#52525b;'>
                📡 &nbsp;Open the sidebar → enter a ticker → hit
                <strong style='color:#a1a1aa;'>Run Analysis</strong>
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p class='example-section-title'>Quick start — click a ticker to select it</p>",
        unsafe_allow_html=True,
    )

    # Clickable rows — clicking sets session state and triggers sidebar to pick it up
    for t, a, w in zip(
        _EXAMPLE_TICKERS["Ticker"],
        _EXAMPLE_TICKERS["Asset"],
        _EXAMPLE_TICKERS["Why"],
    ):
        col_btn, col_asset, col_why = st.columns([1, 2.5, 5])
        with col_btn:
            if st.button(t, key=f"qs_{t}", use_container_width=True):
                st.session_state["selected_ticker"] = t
                st.rerun()
        with col_asset:
            st.markdown(
                f"<span style='font-family:sans-serif;"
                f"font-size:0.82rem;color:#a1a1aa;font-weight:500;"
                f"line-height:2.2;'>{a}</span>",
                unsafe_allow_html=True,
            )
        with col_why:
            st.markdown(
                f"<span style='font-family:sans-serif;"
                f"font-size:0.82rem;color:#52525b;line-height:2.2;'>{w}</span>",
                unsafe_allow_html=True,
            )
        st.markdown(
            "<hr style='margin:0.1rem 0;border-color:rgba(255,255,255,0.04);'/>",
            unsafe_allow_html=True,
        )


# ── Private helpers ───────────────────────────────────────────────────────────

def _desc(text: str) -> None:
    st.markdown(f"<p class='chart-desc'>{text}</p>", unsafe_allow_html=True)