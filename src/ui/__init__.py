"""
src/ui/__init__.py
------------------
UI sub-package for the Stock Market Anomaly Detector.
"""

from .styles  import inject_styles
from .sidebar import render_sidebar
from .header  import render_page_header, render_company_header
from .charts  import render_chart_tabs, render_anomaly_table, render_empty_state

__all__ = [
    "inject_styles",
    "render_sidebar",
    "render_page_header",
    "render_company_header",
    "render_chart_tabs",
    "render_anomaly_table",
    "render_empty_state",
]