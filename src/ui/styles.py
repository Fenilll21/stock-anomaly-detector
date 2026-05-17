"""
src/ui/styles.py
----------------
Global CSS design system for the Stock Market Anomaly Detector.

Call inject_styles() once at the top of app.py, after st.set_page_config().
All design tokens (colours, fonts, radii, spacing) live here — change the
theme in one place and it propagates everywhere.

Fonts loaded (via Google Fonts):
    Syne      – display headings (800, 700, 600)
    DM Sans   – body / UI text  (300, 400, 500)
    DM Mono   – numbers, tickers, metadata (400, 500)
"""

import streamlit as st


def inject_styles() -> None:
    """Inject the full CSS design system into the Streamlit app."""

    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">

        <style>
        /* ── DESIGN TOKENS ─────────────────────────────────────────────── */
        :root {
            --bg-base:        #0a0e1a;
            --bg-surface:     #111827;
            --bg-elevated:    #1a2236;
            --bg-hover:       #1e2d47;
            --border:         rgba(99, 179, 237, 0.12);
            --border-active:  rgba(99, 179, 237, 0.40);
            --accent:         #38bdf8;
            --accent-dim:     rgba(56, 189, 248, 0.15);
            --accent-glow:    rgba(56, 189, 248, 0.25);
            --green:          #34d399;
            --red:            #f87171;
            --amber:          #fbbf24;
            --purple:         #a78bfa;
            --text-primary:   #f0f6ff;
            --text-secondary: #8da3be;
            --text-muted:     #4a6080;
            --font-display:   'Syne', sans-serif;
            --font-body:      'DM Sans', sans-serif;
            --font-mono:      'DM Mono', monospace;
            --radius:         10px;
            --radius-lg:      16px;
        }

        /* ── GLOBAL RESET ───────────────────────────────────────────────── */
        html, body, [class*="css"], .stApp {
            background-color: var(--bg-base) !important;
            color: var(--text-primary) !important;
            font-family: var(--font-body) !important;
        }

        /* ── HIDE STREAMLIT CHROME ──────────────────────────────────────── */
        #MainMenu, footer, header { visibility: hidden; }
        .block-container {
            padding: 2rem 2.5rem 4rem !important;
            max-width: 1400px !important;
        }

        /* ── TYPOGRAPHY ─────────────────────────────────────────────────── */
        h1 {
            font-family: var(--font-display) !important;
            font-weight: 800 !important;
            font-size: 2rem !important;
            letter-spacing: -0.02em !important;
            color: var(--text-primary) !important;
            line-height: 1.15 !important;
        }
        h2, h3 {
            font-family: var(--font-display) !important;
            font-weight: 700 !important;
            color: var(--text-primary) !important;
        }
        h4, h5, h6 {
            font-family: var(--font-display) !important;
            font-weight: 600 !important;
            color: var(--text-secondary) !important;
        }
        p, li, .stMarkdown { color: var(--text-secondary) !important; }

        /* ── SIDEBAR ────────────────────────────────────────────────────── */
        [data-testid="stSidebar"] {
            background-color: var(--bg-surface) !important;
            border-right: 1px solid var(--border) !important;
        }
        [data-testid="stSidebar"] > div:first-child {
            padding: 1.5rem 1.25rem !important;
        }
        [data-testid="stSidebar"] h1 {
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.08em !important;
            text-transform: uppercase !important;
            color: var(--accent) !important;
        }
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            font-family: var(--font-body) !important;
            font-size: 0.7rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.12em !important;
            text-transform: uppercase !important;
            color: var(--text-muted) !important;
            margin-top: 1.25rem !important;
            margin-bottom: 0.5rem !important;
        }
        [data-testid="stSidebar"] hr {
            border: none !important;
            border-top: 1px solid var(--border) !important;
            margin: 1rem 0 !important;
        }

        /* ── INPUTS ─────────────────────────────────────────────────────── */
        [data-testid="stTextInput"] input {
            background: var(--bg-elevated) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius) !important;
            color: var(--text-primary) !important;
            font-family: var(--font-mono) !important;
            font-size: 1.1rem !important;
            font-weight: 500 !important;
            padding: 0.6rem 0.9rem !important;
            transition: border-color 0.2s !important;
        }
        [data-testid="stTextInput"] input:focus {
            border-color: var(--border-active) !important;
            box-shadow: 0 0 0 3px var(--accent-glow) !important;
        }
        [data-testid="stDateInput"] input {
            background: var(--bg-elevated) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius) !important;
            color: var(--text-primary) !important;
            font-family: var(--font-mono) !important;
            font-size: 0.85rem !important;
        }

        /* ── SLIDERS ────────────────────────────────────────────────────── */
        [data-testid="stSlider"] > div > div > div {
            background: var(--accent) !important;
        }
        [data-testid="stSlider"] [data-testid="stThumbValue"] {
            background: var(--accent) !important;
            color: var(--bg-base) !important;
            font-family: var(--font-mono) !important;
            font-size: 0.75rem !important;
            font-weight: 500 !important;
        }

        /* ── BUTTONS ─────────────────────────────────────────────────────── */
        [data-testid="stButton"]:not([data-testid="stButton"]:last-of-type) button {
            background: var(--bg-elevated) !important;
            border: 1px solid var(--border) !important;
            border-radius: 6px !important;
            color: var(--text-secondary) !important;
            font-family: var(--font-mono) !important;
            font-size: 0.75rem !important;
            font-weight: 500 !important;
            padding: 0.3rem 0.5rem !important;
            transition: all 0.15s ease !important;
        }
        [data-testid="stButton"]:not([data-testid="stButton"]:last-of-type) button:hover {
            background: var(--accent-dim) !important;
            border-color: var(--border-active) !important;
            color: var(--accent) !important;
        }
        [data-testid="stButton"] button[kind="primary"] {
            background: var(--accent) !important;
            border: none !important;
            border-radius: var(--radius) !important;
            color: var(--bg-base) !important;
            font-family: var(--font-display) !important;
            font-size: 0.85rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.04em !important;
            text-transform: uppercase !important;
            padding: 0.6rem 1rem !important;
            box-shadow: 0 0 20px var(--accent-glow) !important;
            transition: all 0.2s ease !important;
        }
        [data-testid="stButton"] button[kind="primary"]:hover {
            background: #7dd3fc !important;
            box-shadow: 0 0 30px rgba(56,189,248,0.4) !important;
            transform: translateY(-1px) !important;
        }
        [data-testid="stDownloadButton"] button {
            background: transparent !important;
            border: 1px solid var(--border-active) !important;
            border-radius: var(--radius) !important;
            color: var(--accent) !important;
            font-family: var(--font-body) !important;
            font-size: 0.8rem !important;
            font-weight: 500 !important;
            transition: all 0.15s !important;
        }
        [data-testid="stDownloadButton"] button:hover {
            background: var(--accent-dim) !important;
        }

        /* ── METRIC CARDS ────────────────────────────────────────────────── */
        [data-testid="stMetric"] {
            background: var(--bg-surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-lg) !important;
            padding: 1.1rem 1.25rem !important;
            transition: border-color 0.2s, transform 0.2s !important;
        }
        [data-testid="stMetric"]:hover {
            border-color: var(--border-active) !important;
            transform: translateY(-2px) !important;
        }
        [data-testid="stMetricLabel"] {
            font-family: var(--font-body) !important;
            font-size: 0.7rem !important;
            font-weight: 500 !important;
            letter-spacing: 0.1em !important;
            text-transform: uppercase !important;
            color: var(--text-muted) !important;
        }
        [data-testid="stMetricValue"] {
            font-family: var(--font-display) !important;
            font-size: 1.75rem !important;
            font-weight: 800 !important;
            color: var(--text-primary) !important;
            line-height: 1.2 !important;
        }
        [data-testid="stMetricDelta"] {
            font-family: var(--font-mono) !important;
            font-size: 0.75rem !important;
        }

        /* ── TABS ────────────────────────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {
            background: transparent !important;
            border-bottom: 1px solid var(--border) !important;
            gap: 0 !important;
            padding: 0 !important;
        }
        .stTabs [data-baseweb="tab"] {
            background: transparent !important;
            border: none !important;
            border-bottom: 2px solid transparent !important;
            border-radius: 0 !important;
            color: var(--text-muted) !important;
            font-family: var(--font-body) !important;
            font-size: 0.82rem !important;
            font-weight: 500 !important;
            padding: 0.7rem 1.25rem !important;
            margin-bottom: -1px !important;
            transition: color 0.15s, border-color 0.15s !important;
        }
        .stTabs [data-baseweb="tab"]:hover { color: var(--text-primary) !important; }
        .stTabs [aria-selected="true"] {
            color: var(--accent) !important;
            border-bottom-color: var(--accent) !important;
            background: transparent !important;
        }
        .stTabs [data-baseweb="tab-panel"] {
            background: var(--bg-surface) !important;
            border: 1px solid var(--border) !important;
            border-top: none !important;
            border-radius: 0 0 var(--radius-lg) var(--radius-lg) !important;
            padding: 1.5rem !important;
        }

        /* ── EXPANDER ────────────────────────────────────────────────────── */
        [data-testid="stExpander"] {
            background: var(--bg-surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-lg) !important;
            overflow: hidden !important;
        }
        [data-testid="stExpander"] summary {
            font-family: var(--font-body) !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            color: var(--text-secondary) !important;
            padding: 1rem 1.25rem !important;
            transition: color 0.15s !important;
        }
        [data-testid="stExpander"] summary:hover { color: var(--text-primary) !important; }

        /* ── DATAFRAME ───────────────────────────────────────────────────── */
        [data-testid="stDataFrame"] {
            border-radius: var(--radius) !important;
            overflow: hidden !important;
            border: 1px solid var(--border) !important;
        }
        .dvn-scroller { background: var(--bg-surface) !important; }

        /* ── ALERTS ──────────────────────────────────────────────────────── */
        [data-testid="stAlert"] {
            border-radius: var(--radius-lg) !important;
            border: 1px solid !important;
            font-family: var(--font-body) !important;
            font-size: 0.85rem !important;
        }
        [data-testid="stAlert"][data-baseweb="notification"] {
            background: rgba(248, 113, 113, 0.08) !important;
            border-color: rgba(248, 113, 113, 0.3) !important;
            color: #fca5a5 !important;
        }

        /* ── SPINNER ─────────────────────────────────────────────────────── */
        [data-testid="stSpinner"] p {
            font-family: var(--font-mono) !important;
            font-size: 0.82rem !important;
            color: var(--accent) !important;
        }

        /* ── CAPTIONS ────────────────────────────────────────────────────── */
        [data-testid="stCaptionContainer"] {
            font-family: var(--font-mono) !important;
            font-size: 0.72rem !important;
            color: var(--text-muted) !important;
            letter-spacing: 0.02em !important;
        }

        /* ── DIVIDERS ────────────────────────────────────────────────────── */
        hr {
            border: none !important;
            border-top: 1px solid var(--border) !important;
            margin: 1.25rem 0 !important;
        }

        /* ── COLUMN GAPS ─────────────────────────────────────────────────── */
        [data-testid="stHorizontalBlock"] { gap: 0.75rem !important; }

        /* ── UTILITY CLASSES (used via st.markdown HTML) ─────────────────── */

        .ticker-badge {
            display: inline-block;
            background: var(--accent-dim);
            border: 1px solid var(--border-active);
            border-radius: 6px;
            color: var(--accent);
            font-family: var(--font-mono);
            font-size: 0.85rem;
            font-weight: 500;
            padding: 0.15rem 0.55rem;
            letter-spacing: 0.05em;
            vertical-align: middle;
            margin-left: 0.4rem;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            background: rgba(52, 211, 153, 0.1);
            border: 1px solid rgba(52, 211, 153, 0.3);
            border-radius: 999px;
            color: var(--green);
            font-family: var(--font-mono);
            font-size: 0.7rem;
            font-weight: 500;
            padding: 0.2rem 0.65rem;
            letter-spacing: 0.05em;
        }
        .status-pill::before {
            content: '';
            display: inline-block;
            width: 6px; height: 6px;
            background: var(--green);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50%       { opacity: 0.4; }
        }

        .section-label {
            font-family: var(--font-body);
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 0.85rem;
        }

        .chart-desc {
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border);
        }

        .company-header  { display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem; }
        .company-name    { font-family: var(--font-display); font-size: 1.5rem; font-weight: 800; color: var(--text-primary); }
        .company-meta    { font-family: var(--font-mono); font-size: 0.72rem; color: var(--text-muted); letter-spacing: 0.04em; margin-top: 0.2rem; }
        .meta-sep        { color: var(--border-active); margin: 0 0.35rem; }

        .empty-state {
            text-align: center;
            padding: 4rem 2rem;
            border: 1px dashed var(--border);
            border-radius: var(--radius-lg);
            margin: 2rem 0;
        }
        .empty-state-icon { font-size: 3rem; margin-bottom: 1rem; display: block; }
        .empty-state h3   { font-family: var(--font-display) !important; font-size: 1.1rem !important; font-weight: 700 !important; color: var(--text-primary) !important; margin-bottom: 0.5rem !important; }
        .empty-state p    { color: var(--text-muted) !important; font-size: 0.85rem !important; max-width: 360px; margin: 0 auto; }

        .example-section-title {
            font-family: var(--font-display);
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin: 2rem 0 0.75rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )