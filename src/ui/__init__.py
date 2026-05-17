"""
src/ui/__init__.py
------------------
UI sub-package for the Stock Market Anomaly Detector.

Modules
-------
styles   – inject_styles()          : global CSS design system
controls – render_controls()        : inline horizontal control bar → config dict
header   – render_page_header()     : app title + subtitle
           render_company_header()  : ticker name, badge, KPI metric cards
charts   – render_chart_tabs()      : five analysis tabs + plotly charts
           render_anomaly_table()   : expandable raw anomaly dataframe + CSV download
           render_empty_state()     : placeholder shown before first run
"""

from .styles   import inject_styles
from .controls import render_controls
from .header   import render_page_header, render_company_header
from .charts   import render_chart_tabs, render_anomaly_table, render_empty_state

__all__ = [
    "inject_styles",
    "render_controls",
    "render_page_header",
    "render_company_header",
    "render_chart_tabs",
    "render_anomaly_table",
    "render_empty_state",
]