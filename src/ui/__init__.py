"""
src/ui/__init__.py
------------------
UI sub-package for the Stock Market Anomaly Detector.

Modules
-------
styles   – inject_styles()          : global CSS design system
sidebar  – render_sidebar()         : all sidebar controls → returns config dict
header   – render_page_header()     : app title + subtitle
           render_company_header()  : ticker name, badge, KPI metric cards
charts   – render_chart_tabs()      : five analysis tabs + plotly charts
           render_anomaly_table()   : expandable raw anomaly dataframe + CSV download
"""

from .styles  import inject_styles
from .sidebar import render_sidebar
from .header  import render_page_header, render_company_header
from .charts  import render_chart_tabs, render_anomaly_table

__all__ = [
    "inject_styles",
    "render_sidebar",
    "render_page_header",
    "render_company_header",
    "render_chart_tabs",
    "render_anomaly_table",
]