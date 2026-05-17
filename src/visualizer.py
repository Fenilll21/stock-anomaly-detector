"""
visualizer.py
-------------
All Plotly chart-building functions.

Each function accepts a processed DataFrame (output of anomaly_detector.py)
and returns a plotly.graph_objects.Figure ready for st.plotly_chart().

Keeping visualisation logic here (rather than in app.py) makes the charts
independently testable and keeps the Streamlit file clean.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


# ── Colour palette ──────────────────────────────────────────────────────────
COLOURS = {
    "price":        "#4C9BE8",      # blue — normal price line
    "normal_vol":   "#7FB3D3",      # muted blue — normal volume bars
    "anomaly":      "#E8534C",      # red — anomaly markers
    "zscore_only":  "#F5A623",      # amber — Z-score only anomalies
    "iforest_only": "#9B59B6",      # purple — Isolation Forest only
    "both":         "#E8534C",      # red — caught by both methods
    "grid":         "rgba(200,200,200,0.15)",
    "background":   "#0E1117",      # matches Streamlit dark theme
    "paper":        "#0E1117",
    "text":         "#FAFAFA",
}

ANOMALY_COLOUR_MAP = {
    "Z-Score Only":           COLOURS["zscore_only"],
    "Isolation Forest Only":  COLOURS["iforest_only"],
    "Both Methods":           COLOURS["both"],
}


def _base_layout(title: str, height: int = 450) -> dict:
    """Shared layout settings applied to every chart."""
    return dict(
        title=dict(text=title, font=dict(size=16, color=COLOURS["text"])),
        height=height,
        paper_bgcolor=COLOURS["paper"],
        plot_bgcolor=COLOURS["background"],
        font=dict(color=COLOURS["text"], family="Inter, sans-serif"),
        legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0),
        xaxis=dict(
            gridcolor=COLOURS["grid"],
            showspikes=True, spikecolor="#888", spikethickness=1,
        ),
        yaxis=dict(gridcolor=COLOURS["grid"]),
        hovermode="x unified",
        margin=dict(l=60, r=20, t=60, b=40),
    )


# ── Chart 1: Price + anomaly overlay ───────────────────────────────────────

def plot_price_anomalies(df: pd.DataFrame, ticker: str) -> go.Figure:
    """
    Candlestick chart with anomalous days highlighted as scatter markers.
    Includes a 20-day simple moving average for context.
    """
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        row_heights=[0.7, 0.3],
        vertical_spacing=0.04,
    )

    # ── Candlestick ──────────────────────────────────────────────────────
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"], high=df["High"],
            low=df["Low"],   close=df["Close"],
            name="OHLC",
            increasing_line_color="#26A69A",
            decreasing_line_color="#EF5350",
            showlegend=False,
        ),
        row=1, col=1,
    )

    # ── 20-day SMA ───────────────────────────────────────────────────────
    sma20 = df["Close"].rolling(window=20).mean()
    fig.add_trace(
        go.Scatter(
            x=df.index, y=sma20,
            name="SMA 20",
            line=dict(color="#F5A623", width=1.5, dash="dot"),
        ),
        row=1, col=1,
    )

    # ── Anomaly markers per type ─────────────────────────────────────────
    for atype, colour in ANOMALY_COLOUR_MAP.items():
        mask = df["Anomaly_Type"] == atype
        if mask.any():
            sub = df[mask]
            fig.add_trace(
                go.Scatter(
                    x=sub.index,
                    y=sub["Close"],
                    mode="markers",
                    name=atype,
                    marker=dict(
                        color=colour, size=10,
                        symbol="circle-open", line=dict(width=2),
                    ),
                    hovertemplate=(
                        "<b>%{x|%Y-%m-%d}</b><br>"
                        "Close: $%{y:.2f}<br>"
                        f"Type: {atype}<extra></extra>"
                    ),
                ),
                row=1, col=1,
            )

    # ── Volume bars ──────────────────────────────────────────────────────
    vol_colours = [
        COLOURS["anomaly"] if is_anom else COLOURS["normal_vol"]
        for is_anom in df["Is_Anomaly"]
    ]
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df["Volume"],
            name="Volume",
            marker_color=vol_colours,
            opacity=0.7,
            showlegend=False,
            hovertemplate="<b>%{x|%Y-%m-%d}</b><br>Volume: %{y:,.0f}<extra></extra>",
        ),
        row=2, col=1,
    )

    layout = _base_layout(f"{ticker} — Price & Volume Anomalies", height=600)
    layout["xaxis2"] = dict(gridcolor=COLOURS["grid"])
    layout["yaxis"]  = dict(gridcolor=COLOURS["grid"], title="Price (USD)")
    layout["yaxis2"] = dict(gridcolor=COLOURS["grid"], title="Volume")
    layout["xaxis_rangeslider_visible"] = False

    fig.update_layout(**layout)
    return fig


# ── Chart 2: Z-Score heatmap over time ─────────────────────────────────────

def plot_zscore_heatmap(df: pd.DataFrame) -> go.Figure:
    """
    Line chart showing the Z-scores of all three features over time.
    A horizontal threshold band makes it easy to spot breaches.
    """
    zscore_cols = [c for c in df.columns if c.endswith("_ZScore")]
    feature_names = [c.replace("_ZScore", "").replace("_", " ") for c in zscore_cols]

    fig = go.Figure()

    colours_cycle = ["#4C9BE8", "#26A69A", "#F5A623"]
    for col, label, colour in zip(zscore_cols, feature_names, colours_cycle):
        fig.add_trace(
            go.Scatter(
                x=df.index, y=df[col],
                name=label,
                line=dict(color=colour, width=1.5),
                hovertemplate=f"<b>%{{x|%Y-%m-%d}}</b><br>{label} |Z|: %{{y:.2f}}<extra></extra>",
            )
        )

    # Threshold band — anything above this is anomalous
    max_z = df[zscore_cols].max().max()
    fig.add_hrect(
        y0=2.5, y1=max(max_z * 1.05, 3.0),
        fillcolor="rgba(232, 83, 76, 0.15)",
        line_width=0,
        annotation_text="Anomaly zone",
        annotation_position="top left",
        annotation_font_color=COLOURS["anomaly"],
    )
    fig.add_hline(
        y=2.5,
        line_dash="dash", line_color=COLOURS["anomaly"], line_width=1,
        annotation_text="Z = 2.5",
        annotation_font_color=COLOURS["anomaly"],
    )

    fig.update_layout(
        **_base_layout("Z-Score Over Time by Feature"),
        yaxis_title="|Z-Score|",
    )
    return fig


# ── Chart 3: Isolation Forest anomaly scores ────────────────────────────────

def plot_iforest_scores(df: pd.DataFrame) -> go.Figure:
    """
    Bar chart of Isolation Forest scores (higher = more anomalous).
    Bars are coloured by whether the day was flagged as an anomaly.
    """
    colours = [COLOURS["anomaly"] if a else COLOURS["normal_vol"] for a in df["IForest_Anomaly"]]

    fig = go.Figure(
        go.Bar(
            x=df.index,
            y=df["IForest_Score"],
            marker_color=colours,
            opacity=0.8,
            hovertemplate=(
                "<b>%{x|%Y-%m-%d}</b><br>"
                "Anomaly Score: %{y:.4f}<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        **_base_layout("Isolation Forest Anomaly Scores"),
        yaxis_title="Anomaly Score (higher = more anomalous)",
        showlegend=False,
    )
    return fig


# ── Chart 4: Return distribution ────────────────────────────────────────────

def plot_return_distribution(df: pd.DataFrame) -> go.Figure:
    """
    Histogram of daily returns, with anomalous returns overlaid in red.
    Helps visualise whether anomalies cluster in the tails.
    """
    fig = go.Figure()

    normal_returns  = df.loc[~df["Is_Anomaly"], "Daily_Return"]
    anomaly_returns = df.loc[ df["Is_Anomaly"], "Daily_Return"]

    fig.add_trace(
        go.Histogram(
            x=normal_returns,
            name="Normal",
            marker_color=COLOURS["price"],
            opacity=0.7,
            nbinsx=50,
        )
    )
    fig.add_trace(
        go.Histogram(
            x=anomaly_returns,
            name="Anomaly",
            marker_color=COLOURS["anomaly"],
            opacity=0.9,
            nbinsx=30,
        )
    )

    fig.update_layout(
        **_base_layout("Daily Return Distribution — Normal vs Anomalous"),
        barmode="overlay",
        xaxis_title="Daily Return (%)",
        yaxis_title="Count",
    )
    return fig


# ── Chart 5: Anomaly calendar heatmap ──────────────────────────────────────

def plot_anomaly_scatter(df: pd.DataFrame) -> go.Figure:
    """
    Scatter plot of Daily Return vs Volume, coloured by anomaly status.
    Shows the feature space where anomalies live relative to normal data.
    """
    fig = px.scatter(
        df.reset_index(),
        x="Volume",
        y="Daily_Return",
        color="Anomaly_Type",
        color_discrete_map={
            "Normal":                 COLOURS["normal_vol"],
            "Z-Score Only":           COLOURS["zscore_only"],
            "Isolation Forest Only":  COLOURS["iforest_only"],
            "Both Methods":           COLOURS["both"],
        },
        hover_data={"Date": True, "Close": True},
        labels={"Daily_Return": "Daily Return (%)", "Volume": "Volume"},
        title="Feature Space: Daily Return vs Volume",
        template="plotly_dark",
        opacity=0.75,
    )

    fig.update_layout(
        **_base_layout("Feature Space — Return vs Volume"),
        xaxis_title="Volume",
        yaxis_title="Daily Return (%)",
    )
    return fig
