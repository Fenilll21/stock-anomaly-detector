"""
src/ui/styles.py
----------------
Global CSS design system for the Stock Market Anomaly Detector.

Theme: Light grey canvas — Vercel/GitHub aesthetic.
Base colours are set in .streamlit/config.toml; this file handles
typography, spacing, component polish, and utility classes only.
No visibility/display overrides on Streamlit chrome elements.

Call inject_styles() once at the top of app.py, after set_page_config().
"""

import streamlit as st


def inject_styles() -> None:
    """Inject the full CSS design system into the Streamlit app."""

    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500&family=Geist:wght@400;500;600;700&display=swap" rel="stylesheet">

        <style>
        /* ── DESIGN TOKENS ─────────────────────────────────────────────── */
        :root {
            --bg-base:        #f6f8fa;
            --bg-surface:     #ffffff;
            --bg-elevated:    #f0f3f6;
            --bg-hover:       #eaeef2;
            --border:         #d0d7de;
            --border-active:  #0969da;
            --accent:         #0969da;
            --accent-dim:     rgba(9, 105, 218, 0.08);
            --accent-glow:    rgba(9, 105, 218, 0.15);
            --green:          #1a7f37;
            --green-bg:       #dafbe1;
            --red:            #cf222e;
            --red-bg:         #ffebe9;
            --amber:          #9a6700;
            --amber-bg:       #fff8c5;
            --purple:         #8250df;
            --text-primary:   #1c2128;
            --text-secondary: #57606a;
            --text-muted:     #8c959f;
            --font-display:   'Geist', sans-serif;
            --font-body:      'Geist', sans-serif;
            --font-mono:      'Geist Mono', monospace;
            --radius:         6px;
            --radius-lg:      10px;
            --shadow-sm:      0 1px 3px rgba(31,35,40,0.08), 0 0 0 1px rgba(31,35,40,0.06);
            --shadow-md:      0 3px 8px rgba(31,35,40,0.12), 0 0 0 1px rgba(31,35,40,0.06);
        }

        /* ── GLOBAL ──────────────────────────────────────────────────── */
        html, body, .stApp {
            background-color: var(--bg-base) !important;
            font-family: var(--font-body) !important;
            color: var(--text-primary) !important;
        }

        /* ── LAYOUT ──────────────────────────────────────────────────── */
        .block-container {
            padding-top: 4rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            padding-bottom: 3rem !important;
            max-width: 1280px !important;
        }

        /* Fade deploy/menu — opacity only, no layout disruption */
        [data-testid="stDeployButton"],
        #MainMenu {
            opacity: 0 !important;
            pointer-events: none !important;
        }
        header:hover [data-testid="stDeployButton"],
        header:hover #MainMenu {
            opacity: 0.4 !important;
            pointer-events: auto !important;
        }
        header[data-testid="stHeader"] {
            background: var(--bg-base) !important;
            border-bottom: 1px solid var(--border) !important;
        }

        /* ── TYPOGRAPHY ──────────────────────────────────────────────── */
        h1, h2, h3, h4, h5, h6 {
            font-family: var(--font-display) !important;
            color: var(--text-primary) !important;
            letter-spacing: -0.01em !important;
        }
        h1 { font-size: 1.6rem !important; font-weight: 700 !important; }
        h2 { font-size: 1.2rem !important; font-weight: 600 !important; }
        h3 { font-size: 1rem   !important; font-weight: 600 !important; }
        p, li { color: var(--text-secondary) !important; font-size: 0.875rem !important; }

        /* Hide anchor icons on headings */
        .stMarkdown h1 a, .stMarkdown h2 a,
        .stMarkdown h3 a, .stMarkdown h4 a { display: none !important; }

        /* ── SIDEBAR (hidden — controls are inline) ───────────────────── */
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="stSidebarCollapsedControl"] { display: none !important; }

        /* ── CONTROL BAR ─────────────────────────────────────────────── */
        .control-bar {
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 1rem 1.25rem;
            margin-bottom: 1.5rem;
            box-shadow: var(--shadow-sm);
        }
        .control-bar-title {
            font-family: var(--font-mono);
            font-size: 0.65rem;
            font-weight: 500;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 0.75rem;
        }

        /* ── INPUTS ──────────────────────────────────────────────────── */
        [data-testid="stTextInput"] input {
            background: var(--bg-base) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius) !important;
            color: var(--text-primary) !important;
            font-family: var(--font-mono) !important;
            font-size: 0.95rem !important;
            font-weight: 500 !important;
            padding: 0.4rem 0.7rem !important;
            transition: border-color 0.15s, box-shadow 0.15s !important;
        }
        [data-testid="stTextInput"] input:focus {
            border-color: var(--border-active) !important;
            box-shadow: 0 0 0 3px var(--accent-glow) !important;
            outline: none !important;
        }

        [data-testid="stDateInput"] input {
            background: var(--bg-base) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius) !important;
            color: var(--text-primary) !important;
            font-family: var(--font-mono) !important;
            font-size: 0.8rem !important;
            padding: 0.35rem 0.6rem !important;
        }

        /* Number inputs for compact sliders */
        [data-testid="stNumberInput"] input {
            background: var(--bg-base) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius) !important;
            color: var(--text-primary) !important;
            font-family: var(--font-mono) !important;
            font-size: 0.85rem !important;
            padding: 0.35rem 0.6rem !important;
        }

        /* ── BUTTONS ─────────────────────────────────────────────────── */
        /* Quick-pick ticker chips */
        [data-testid="stButton"] button {
            background: var(--bg-base) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius) !important;
            color: var(--text-secondary) !important;
            font-family: var(--font-mono) !important;
            font-size: 0.72rem !important;
            font-weight: 500 !important;
            padding: 0.25rem 0.6rem !important;
            transition: all 0.12s ease !important;
            box-shadow: none !important;
        }
        [data-testid="stButton"] button:hover {
            background: var(--accent-dim) !important;
            border-color: var(--accent) !important;
            color: var(--accent) !important;
        }

        /* Primary run button */
        [data-testid="stButton"] button[kind="primary"] {
            background: var(--accent) !important;
            border: none !important;
            border-radius: var(--radius) !important;
            color: #ffffff !important;
            font-family: var(--font-display) !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            padding: 0.45rem 1.1rem !important;
            letter-spacing: 0.01em !important;
            box-shadow: var(--shadow-sm) !important;
            transition: background 0.15s, box-shadow 0.15s !important;
        }
        [data-testid="stButton"] button[kind="primary"]:hover {
            background: #0860c8 !important;
            box-shadow: var(--shadow-md) !important;
        }

        /* Download button */
        [data-testid="stDownloadButton"] button {
            background: var(--bg-surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius) !important;
            color: var(--accent) !important;
            font-family: var(--font-body) !important;
            font-size: 0.78rem !important;
            font-weight: 500 !important;
            padding: 0.35rem 0.75rem !important;
            transition: background 0.12s !important;
        }
        [data-testid="stDownloadButton"] button:hover {
            background: var(--accent-dim) !important;
            border-color: var(--accent) !important;
        }

        /* ── SLIDERS ─────────────────────────────────────────────────── */
        [data-testid="stSlider"] > div > div > div {
            background: var(--accent) !important;
        }
        [data-testid="stSlider"] [data-testid="stThumbValue"] {
            background: var(--accent) !important;
            color: #fff !important;
            font-family: var(--font-mono) !important;
            font-size: 0.7rem !important;
        }

        /* ── METRIC CARDS ────────────────────────────────────────────── */
        [data-testid="stMetric"] {
            background: var(--bg-surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-lg) !important;
            padding: 0.85rem 1rem !important;
            box-shadow: var(--shadow-sm) !important;
            transition: box-shadow 0.15s, border-color 0.15s !important;
        }
        [data-testid="stMetric"]:hover {
            box-shadow: var(--shadow-md) !important;
            border-color: #b1bac4 !important;
        }
        [data-testid="stMetricLabel"] {
            font-family: var(--font-body) !important;
            font-size: 0.68rem !important;
            font-weight: 500 !important;
            letter-spacing: 0.06em !important;
            text-transform: uppercase !important;
            color: var(--text-muted) !important;
        }
        [data-testid="stMetricValue"] {
            font-family: var(--font-display) !important;
            font-size: 1.45rem !important;
            font-weight: 700 !important;
            color: var(--text-primary) !important;
            line-height: 1.2 !important;
        }
        [data-testid="stMetricDelta"] {
            font-family: var(--font-mono) !important;
            font-size: 0.72rem !important;
        }

        /* ── TABS ────────────────────────────────────────────────────── */
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
            font-size: 0.8rem !important;
            font-weight: 500 !important;
            padding: 0.55rem 1rem !important;
            margin-bottom: -1px !important;
            transition: color 0.12s !important;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: var(--text-primary) !important;
            background: var(--bg-hover) !important;
        }
        .stTabs [aria-selected="true"] {
            color: var(--accent) !important;
            border-bottom-color: var(--accent) !important;
            background: transparent !important;
            font-weight: 600 !important;
        }
        .stTabs [data-baseweb="tab-panel"] {
            background: var(--bg-surface) !important;
            border: 1px solid var(--border) !important;
            border-top: none !important;
            border-radius: 0 0 var(--radius-lg) var(--radius-lg) !important;
            padding: 1.25rem !important;
        }

        /* ── EXPANDER ────────────────────────────────────────────────── */
        [data-testid="stExpander"] {
            background: var(--bg-surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-lg) !important;
            box-shadow: var(--shadow-sm) !important;
            overflow: hidden !important;
        }
        [data-testid="stExpander"] summary {
            font-family: var(--font-body) !important;
            font-size: 0.82rem !important;
            font-weight: 500 !important;
            color: var(--text-secondary) !important;
            padding: 0.75rem 1rem !important;
        }
        [data-testid="stExpander"] summary:hover {
            color: var(--text-primary) !important;
            background: var(--bg-hover) !important;
        }

        /* ── DATAFRAME ───────────────────────────────────────────────── */
        [data-testid="stDataFrame"] {
            border: 1px solid var(--border) !important;
            border-radius: var(--radius) !important;
            overflow: hidden !important;
        }

        /* ── ALERTS ──────────────────────────────────────────────────── */
        [data-testid="stAlert"] {
            border-radius: var(--radius-lg) !important;
            font-family: var(--font-body) !important;
            font-size: 0.82rem !important;
            border: 1px solid !important;
        }

        /* ── SPINNER ─────────────────────────────────────────────────── */
        [data-testid="stSpinner"] p {
            font-family: var(--font-mono) !important;
            font-size: 0.78rem !important;
            color: var(--text-secondary) !important;
        }

        /* ── CAPTIONS ────────────────────────────────────────────────── */
        [data-testid="stCaptionContainer"] {
            font-family: var(--font-mono) !important;
            font-size: 0.68rem !important;
            color: var(--text-muted) !important;
        }

        /* ── DIVIDERS ────────────────────────────────────────────────── */
        hr {
            border: none !important;
            border-top: 1px solid var(--border) !important;
            margin: 1rem 0 !important;
        }

        /* ── COLUMN GAPS ─────────────────────────────────────────────── */
        [data-testid="stHorizontalBlock"] { gap: 0.5rem !important; }

        /* ── UTILITY CLASSES (via st.markdown HTML) ──────────────────── */

        .page-title {
            font-family: var(--font-display);
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.02em;
            display: inline;
        }
        .page-title-accent {
            font-family: var(--font-display);
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--accent);
            letter-spacing: -0.02em;
            display: inline;
        }
        .page-subtitle {
            font-size: 0.82rem;
            color: var(--text-muted);
            margin-top: 0.2rem;
        }

        .ticker-badge {
            display: inline-block;
            background: var(--accent-dim);
            border: 1px solid rgba(9,105,218,0.25);
            border-radius: 4px;
            color: var(--accent);
            font-family: var(--font-mono);
            font-size: 0.75rem;
            font-weight: 500;
            padding: 0.1rem 0.45rem;
            letter-spacing: 0.03em;
            vertical-align: middle;
            margin-left: 0.35rem;
        }

        .company-name {
            font-family: var(--font-display);
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--text-primary);
        }
        .company-meta {
            font-family: var(--font-mono);
            font-size: 0.68rem;
            color: var(--text-muted);
            margin-top: 0.15rem;
        }
        .meta-sep { color: var(--border); margin: 0 0.3rem; }

        .section-label {
            font-family: var(--font-mono);
            font-size: 0.65rem;
            font-weight: 500;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 0.65rem;
        }

        .chart-desc {
            font-size: 0.78rem;
            color: var(--text-muted);
            margin-bottom: 0.85rem;
            padding-bottom: 0.85rem;
            border-bottom: 1px solid var(--border);
        }

        .empty-state {
            text-align: center;
            padding: 3.5rem 2rem;
            border: 1px dashed var(--border);
            border-radius: var(--radius-lg);
            margin: 1rem 0;
            background: var(--bg-surface);
        }
        .empty-state-icon { font-size: 2.5rem; margin-bottom: 0.75rem; display: block; }
        .empty-state h3 {
            font-family: var(--font-display) !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            color: var(--text-primary) !important;
            margin-bottom: 0.35rem !important;
        }
        .empty-state p {
            color: var(--text-muted) !important;
            font-size: 0.8rem !important;
            max-width: 320px;
            margin: 0 auto !important;
        }

        .example-table {
            width: 100%;
            border-collapse: collapse;
            font-family: var(--font-body);
            font-size: 0.82rem;
            margin-top: 0.5rem;
        }
        .example-table th {
            text-align: left;
            font-size: 0.65rem;
            font-weight: 500;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--text-muted);
            padding: 0.5rem 0.85rem;
            border-bottom: 1px solid var(--border);
            background: var(--bg-elevated);
        }
        .example-table td {
            padding: 0.55rem 0.85rem;
            border-bottom: 1px solid var(--border);
            color: var(--text-secondary);
        }
        .example-table tr:last-child td { border-bottom: none; }
        .example-table tr:hover td {
            background: var(--bg-elevated);
            cursor: default;
        }

        .example-section-title {
            font-family: var(--font-mono);
            font-size: 0.65rem;
            font-weight: 500;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-muted);
            margin: 1.5rem 0 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )