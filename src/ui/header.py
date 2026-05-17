"""
src/ui/header.py
----------------
Page header components:

  render_page_header()          – app title + subtitle
  render_live_price_banner()    – live price strip for one or two tickers
  render_home_button()          – reset session state → back to empty state
  render_company_header()       – company name, badge, KPI metric cards
"""

import streamlit as st
import yfinance as yf


# ── Public API ────────────────────────────────────────────────────────────────

def render_page_header() -> None:
    """App title + subtitle + home button row."""
    col_title, col_home = st.columns([10, 1])

    with col_title:
        st.markdown(
            """
            <div style='margin-bottom:0.25rem;'>
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

    with col_home:
        # Always visible — active when results/error exist, dimmed otherwise
        has_content = (
            bool(st.session_state.get("results")) or
            bool(st.session_state.get("error"))
        )
        btn_style = "" if has_content else (
            "opacity:0.3;pointer-events:none;"
        )
        st.markdown(
            f"<div style='padding-top:0.25rem;{btn_style}'>",
            unsafe_allow_html=True,
        )
        if st.button(
            "⌂ Home",
            help="Reset — go back to the start",
            key="home_btn",
            use_container_width=True,
            disabled=not has_content,
        ):
            st.session_state["results"] = None
            st.session_state["error"]   = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def render_live_price_banner(ticker_a: str, ticker_b: str = "") -> None:
    """
    Slim live price strip — only shown after analysis has been run.
    Fetches current price + daily % change via yfinance.

    Parameters
    ----------
    ticker_a : str   – primary ticker
    ticker_b : str   – comparison ticker (empty string = single mode)
    """
    # Only show once results exist — not on initial empty state load
    if not st.session_state.get("results"):
        return

    tickers = [t for t in [ticker_a, ticker_b] if t]
    if not tickers:
        return

    prices = [_fetch_live(t) for t in tickers]

    cols = st.columns(len(tickers) + 1)   # +1 for the label column

    with cols[0]:
        st.markdown(
            "<div style='font-family:\"JetBrains Mono\",monospace;"
            "font-size:0.62rem;color:#52525b;padding-top:0.35rem;"
            "letter-spacing:0.08em;'>LIVE</div>",
            unsafe_allow_html=True,
        )

    for col, ticker, data in zip(cols[1:], tickers, prices):
        with col:
            if data:
                change_colour = "#22c55e" if data["change"] >= 0 else "#ef4444"
                arrow         = "▲" if data["change"] >= 0 else "▼"
                st.markdown(
                    f"""
                    <div style='display:flex;align-items:center;gap:0.6rem;
                                font-family:"JetBrains Mono",monospace;'>
                        <span style='font-size:0.72rem;color:#a1a1aa;
                                     font-weight:500;letter-spacing:0.04em;'>
                            {ticker}
                        </span>
                        <span style='font-size:0.9rem;color:#fff;font-weight:500;'>
                            ${data["price"]:.2f}
                        </span>
                        <span style='font-size:0.72rem;color:{change_colour};font-weight:500;'>
                            {arrow} {abs(data["change"]):.2f}%
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<span style='font-family:\"JetBrains Mono\",monospace;"
                    f"font-size:0.72rem;color:#52525b;'>{ticker} — unavailable</span>",
                    unsafe_allow_html=True,
                )


def render_company_header(info: dict, ticker: str, summary: dict) -> None:
    """
    Company name, ticker badge, metadata row, and KPI metric cards.

    Parameters
    ----------
    info    : dict  – name, sector, exchange, currency
    ticker  : str   – upper-cased symbol
    summary : dict  – total_days, total_anomalies, anomaly_rate,
                      zscore_only, iforest_only, both_methods, worst_return
    """
    _render_company_name(info, ticker)
    st.markdown("<hr style='margin:0.75rem 0'/>", unsafe_allow_html=True)
    _render_kpi_cards(summary)
    st.markdown("<hr style='margin:1rem 0'/>", unsafe_allow_html=True)


# ── Private helpers ───────────────────────────────────────────────────────────

def _fetch_live(ticker: str) -> dict | None:
    """
    Fetch current price and daily % change from yfinance.
    Returns None if the fetch fails (e.g. no internet, bad ticker).
    """
    try:
        tk   = yf.Ticker(ticker)
        info = tk.fast_info
        price  = float(info.last_price)
        prev   = float(info.previous_close)
        change = ((price - prev) / prev) * 100
        return {"price": price, "change": change}
    except Exception:
        return None


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