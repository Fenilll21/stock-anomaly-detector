"""
src/ui/styles.py
----------------
Global CSS design system — Linear/Vercel dark aesthetic.
Deep black canvas · electric blue accent · razor-thin borders.

Call inject_styles() once in app.py after set_page_config().
Base colours are in .streamlit/config.toml.
This file handles typography, spacing, and component polish only —
no display/visibility overrides on Streamlit chrome.
"""

import streamlit as st


def inject_styles() -> None:
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

        <style>
        /* ── TOKENS ──────────────────────────────────────────────────── */
        :root {
            --bg:           #0a0a0a;
            --surface:      #111111;
            --elevated:     #1a1a1a;
            --border:       rgba(255,255,255,0.07);
            --border-hover: rgba(255,255,255,0.15);
            --accent:       #2563eb;
            --accent-dim:   rgba(37,99,235,0.12);
            --accent-hover: #1d4ed8;
            --green:        #22c55e;
            --red:          #ef4444;
            --amber:        #f59e0b;
            --text-1:       #ffffff;
            --text-2:       #a1a1aa;
            --text-3:       #52525b;
            --font:         'Plus Jakarta Sans', sans-serif;
            --mono:         'JetBrains Mono', monospace;
            --radius:       6px;
            --radius-lg:    10px;
        }

        /* ── BASE ────────────────────────────────────────────────────── */
        html, body, .stApp {
            background: var(--bg) !important;
            font-family: var(--font) !important;
            color: var(--text-1) !important;
        }

        /* ── LAYOUT ──────────────────────────────────────────────────── */
        .block-container {
            padding: 4.5rem 2.5rem 3rem !important;
            max-width: 1300px !important;
        }
        [data-testid="stHorizontalBlock"] { gap: 0.6rem !important; }

        /* ── HEADER / CHROME ─────────────────────────────────────────── */
        header[data-testid="stHeader"] {
            background: rgba(10,10,10,0.85) !important;
            backdrop-filter: blur(12px) !important;
            border-bottom: 1px solid var(--border) !important;
        }
        /* Fade deploy — opacity only, never display:none on chrome */
        [data-testid="stDeployButton"] { opacity: 0 !important; pointer-events: none !important; }
        header:hover [data-testid="stDeployButton"] { opacity: 0.25 !important; pointer-events: auto !important; }

        /* ── SIDEBAR ─────────────────────────────────────────────────── */
        [data-testid="stSidebar"] {
            background: var(--surface) !important;
            border-right: 1px solid var(--border) !important;
        }
        [data-testid="stSidebar"] > div:first-child {
            padding: 1.25rem 1rem !important;
        }

        /* ── TYPOGRAPHY ──────────────────────────────────────────────── */
        h1,h2,h3,h4,h5,h6 {
            font-family: var(--font) !important;
            color: var(--text-1) !important;
            letter-spacing: -0.02em !important;
        }
        p, li, .stMarkdown { color: var(--text-2) !important; font-size: 0.875rem !important; }
        .stMarkdown h1 a, .stMarkdown h2 a,
        .stMarkdown h3 a, .stMarkdown h4 a { display: none !important; }

        /* ── INPUTS ──────────────────────────────────────────────────── */
        [data-testid="stTextInput"] input,
        [data-testid="stDateInput"] input,
        [data-testid="stNumberInput"] input {
            background: var(--elevated) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius) !important;
            color: var(--text-1) !important;
            font-family: var(--mono) !important;
            font-size: 0.85rem !important;
            padding: 0.45rem 0.75rem !important;
            transition: border-color 0.15s !important;
        }
        [data-testid="stTextInput"] input:focus,
        [data-testid="stDateInput"] input:focus,
        [data-testid="stNumberInput"] input:focus {
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 3px var(--accent-dim) !important;
            outline: none !important;
        }

        /* ── SLIDERS ─────────────────────────────────────────────────── */
        /* Accent colour on the filled track portion only */
        [data-testid="stSlider"] [role="slider"] { background: var(--accent) !important; }
        [data-testid="stSlider"] > div > div > div > div:first-child {
            background: var(--accent) !important;
        }
        /* Thumb tooltip value */
        [data-testid="stSlider"] [data-testid="stThumbValue"] {
            background: var(--accent) !important;
            color: #fff !important;
            font-family: var(--mono) !important;
            font-size: 0.7rem !important;
        }
        /* Min/max labels — always visible, no highlight */
        [data-testid="stTickBarMin"],
        [data-testid="stTickBarMax"] {
            background: transparent !important;
            color: var(--text-3) !important;
            font-family: var(--mono) !important;
            font-size: 0.68rem !important;
            padding: 0 !important;
            opacity: 1 !important;
            visibility: visible !important;
            display: block !important;
        }
        /* Streamlit hides these on non-hover — force always shown */
        [data-testid="stSlider"]:not(:hover) [data-testid="stTickBarMin"],
        [data-testid="stSlider"]:not(:hover) [data-testid="stTickBarMax"] {
            opacity: 1 !important;
            visibility: visible !important;
            display: block !important;
        }

        /* ── BUTTONS ─────────────────────────────────────────────────── */
        [data-testid="stButton"] button {
            background: var(--elevated) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius) !important;
            color: var(--text-2) !important;
            font-family: var(--font) !important;
            font-size: 0.75rem !important;
            font-weight: 500 !important;
            padding: 0.3rem 0.65rem !important;
            transition: all 0.15s !important;
        }
        [data-testid="stButton"] button:hover {
            background: var(--accent-dim) !important;
            border-color: var(--accent) !important;
            color: var(--accent) !important;
        }
        [data-testid="stButton"] button[kind="primary"] {
            background: transparent !important;
            border: 1.5px solid var(--accent) !important;
            color: var(--accent) !important;
            font-weight: 600 !important;
            font-size: 0.8rem !important;
            padding: 0.45rem 1.1rem !important;
            letter-spacing: 0.01em !important;
            box-shadow: none !important;
        }
        [data-testid="stButton"] button[kind="primary"]:hover {
            background: var(--accent-dim) !important;
            border-color: var(--accent) !important;
            color: var(--accent) !important;
        }
        [data-testid="stDownloadButton"] button {
            background: transparent !important;
            border: 1px solid var(--border-hover) !important;
            color: var(--accent) !important;
            font-size: 0.78rem !important;
        }
        [data-testid="stDownloadButton"] button:hover {
            background: var(--accent-dim) !important;
        }

        /* ── METRIC CARDS ────────────────────────────────────────────── */
        [data-testid="stMetric"] {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-lg) !important;
            padding: 1rem 1.1rem !important;
            transition: border-color 0.2s !important;
        }
        [data-testid="stMetric"]:hover {
            border-color: var(--border-hover) !important;
        }
        [data-testid="stMetricLabel"] {
            font-family: var(--font) !important;
            font-size: 0.68rem !important;
            font-weight: 500 !important;
            letter-spacing: 0.06em !important;
            text-transform: uppercase !important;
            color: var(--text-3) !important;
        }
        [data-testid="stMetricValue"] {
            font-family: var(--mono) !important;
            font-size: 1.5rem !important;
            font-weight: 500 !important;
            color: var(--text-1) !important;
            line-height: 1.2 !important;
        }
        [data-testid="stMetricDelta"] {
            font-family: var(--mono) !important;
            font-size: 0.7rem !important;
        }

        /* ── TABS ────────────────────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {
            background: transparent !important;
            border-bottom: 1px solid var(--border) !important;
            gap: 0 !important; padding: 0 !important;
        }
        .stTabs [data-baseweb="tab"] {
            background: transparent !important;
            border: none !important;
            border-bottom: 2px solid transparent !important;
            border-radius: 0 !important;
            color: var(--text-3) !important;
            font-family: var(--font) !important;
            font-size: 0.8rem !important;
            font-weight: 500 !important;
            padding: 0.6rem 1.1rem !important;
            margin-bottom: -1px !important;
            transition: color 0.15s !important;
        }
        .stTabs [data-baseweb="tab"]:hover { color: var(--text-1) !important; }
        .stTabs [aria-selected="true"] {
            color: var(--accent) !important;
            border-bottom-color: var(--accent) !important;
            font-weight: 600 !important;
        }
        .stTabs [data-baseweb="tab-panel"] {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-top: none !important;
            border-radius: 0 0 var(--radius-lg) var(--radius-lg) !important;
            padding: 1.25rem !important;
        }

        /* ── EXPANDER ────────────────────────────────────────────────── */
        [data-testid="stExpander"] {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-lg) !important;
        }
        [data-testid="stExpander"] summary {
            font-family: var(--font) !important;
            font-size: 0.82rem !important;
            font-weight: 500 !important;
            color: var(--text-2) !important;
            padding: 0.8rem 1rem !important;
        }
        [data-testid="stExpander"] summary:hover { color: var(--text-1) !important; }

        /* ── DATAFRAME ───────────────────────────────────────────────── */
        [data-testid="stDataFrame"] {
            border: 1px solid var(--border) !important;
            border-radius: var(--radius) !important;
        }

        /* ── ALERTS ──────────────────────────────────────────────────── */
        [data-testid="stAlert"] {
            border-radius: var(--radius-lg) !important;
            font-family: var(--font) !important;
            font-size: 0.82rem !important;
        }

        /* ── SPINNER / CAPTION ───────────────────────────────────────── */
        [data-testid="stSpinner"] p { font-family: var(--mono) !important; font-size: 0.78rem !important; color: var(--text-2) !important; }
        [data-testid="stCaptionContainer"] { font-family: var(--mono) !important; font-size: 0.68rem !important; color: var(--text-3) !important; }

        /* ── DIVIDERS ────────────────────────────────────────────────── */
        hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 1rem 0 !important; }

        /* ════════════════════════════════════════════════════════════════
           UTILITY CLASSES  (used in st.markdown HTML blocks)
           ════════════════════════════════════════════════════════════════ */

        /* Page title */
        .page-title {
            font-family: var(--font);
            font-size: 1.35rem;
            font-weight: 700;
            color: var(--text-1);
            letter-spacing: -0.03em;
            line-height: 1.2;
        }
        .page-title em {
            color: var(--accent);
            font-style: normal;
        }
        .page-subtitle {
            font-family: var(--font);
            font-size: 0.8rem;
            color: var(--text-3);
            margin-top: 0.25rem;
            font-weight: 400;
        }

        /* Ticker badge */
        .ticker-badge {
            display: inline-block;
            background: var(--accent-dim);
            border: 1px solid rgba(37,99,235,0.3);
            border-radius: 4px;
            color: var(--accent);
            font-family: var(--mono);
            font-size: 0.72rem;
            font-weight: 500;
            padding: 0.1rem 0.45rem;
            letter-spacing: 0.04em;
            vertical-align: middle;
            margin-left: 0.4rem;
        }

        /* Company header */
        .company-name {
            font-family: var(--font);
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-1);
            letter-spacing: -0.02em;
        }
        .company-meta {
            font-family: var(--mono);
            font-size: 0.68rem;
            color: var(--text-3);
            margin-top: 0.15rem;
            letter-spacing: 0.02em;
        }
        .meta-sep { color: var(--border-hover); margin: 0 0.3rem; }

        /* Section label */
        .section-label {
            font-family: var(--mono);
            font-size: 0.62rem;
            font-weight: 500;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--text-3);
            margin-bottom: 0.65rem;
        }

        /* Chart description */
        .chart-desc {
            font-size: 0.78rem;
            color: var(--text-3);
            margin-bottom: 1rem;
            padding-bottom: 0.85rem;
            border-bottom: 1px solid var(--border);
        }

        /* Empty state */
        .empty-state {
            text-align: center;
            padding: 4rem 2rem;
            border: 1px dashed rgba(255,255,255,0.07);
            border-radius: var(--radius-lg);
            background: var(--surface);
            margin: 0.5rem 0;
        }
        .empty-state-icon { font-size: 2.5rem; margin-bottom: 1rem; display: block; }
        .empty-state h3 {
            font-family: var(--font) !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            color: var(--text-1) !important;
            letter-spacing: -0.02em !important;
            margin-bottom: 0.4rem !important;
        }
        .empty-state p {
            font-size: 0.8rem !important;
            color: var(--text-3) !important;
            max-width: 300px;
            margin: 0 auto !important;
            line-height: 1.6 !important;
        }

        /* Suggested tickers table */
        .example-table {
            width: 100%;
            border-collapse: collapse;
            font-family: var(--font);
            font-size: 0.82rem;
            margin-top: 0.75rem;
        }
        .example-table th {
            text-align: left;
            font-size: 0.62rem;
            font-weight: 500;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-3);
            padding: 0.5rem 0.9rem;
            border-bottom: 1px solid var(--border);
        }
        .example-table td {
            padding: 0.6rem 0.9rem;
            border-bottom: 1px solid var(--border);
            color: var(--text-2);
        }
        .example-table tr:last-child td { border-bottom: none; }
        .example-table tr:hover td { background: var(--elevated); }

        .example-section-title {
            font-family: var(--mono);
            font-size: 0.62rem;
            font-weight: 500;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--text-3);
            margin: 1.5rem 0 0.5rem;
        }

        /* Sidebar section label */
        .sidebar-section {
            font-family: var(--mono);
            font-size: 0.6rem;
            font-weight: 500;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--text-3);
            margin: 1.1rem 0 0.4rem;
            padding-bottom: 0.4rem;
            border-bottom: 1px solid var(--border);
        }
        /* ── RESPONSIVE ─────────────────────────────────────────────── */

        /* Tighten padding on smaller screens */
        @media (max-width: 1200px) {
            .block-container {
                padding-left: 1.5rem !important;
                padding-right: 1.5rem !important;
            }
        }

        /* Stack metric cards into 3 cols on medium screens */
        @media (max-width: 1100px) {
            [data-testid="stMetric"] {
                min-width: 140px !important;
            }
        }

        /* Timeline cards: smaller on tighter viewports */
        @media (max-width: 900px) {
            .block-container {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }
        }

        /* Sidebar: tighter padding on small screens */
        @media (max-width: 768px) {
            [data-testid="stSidebar"] > div:first-child {
                padding: 1rem 0.75rem !important;
            }
            [data-testid="stMetricValue"] {
                font-size: 1.2rem !important;
            }
        }

        /* Smooth sidebar slide transition */
        [data-testid="stSidebar"] {
            transition: transform 0.25s ease, width 0.25s ease !important;
        }

        /* Smooth page content shift when sidebar opens/closes */
        .main .block-container {
            transition: padding 0.25s ease !important;
        }

        /* Prevent horizontal overflow on small screens */
        .stApp {
            overflow-x: hidden !important;
        }

        /* Scrollbar styling — thin and dark */
        ::-webkit-scrollbar { width: 4px; height: 4px; }
        ::-webkit-scrollbar-track { background: var(--bg); }
        ::-webkit-scrollbar-thumb {
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255,255,255,0.2);
        }

        </style>
        """,
        unsafe_allow_html=True,
    )