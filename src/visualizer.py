"""
visualizer.py
-------------
All Plotly chart-building functions — deep black dark theme.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

COLOURS = {
    "price":        "#3b82f6",
    "normal_vol":   "#1e3a5f",
    "anomaly":      "#ef4444",
    "zscore_only":  "#f59e0b",
    "iforest_only": "#8b5cf6",
    "both":         "#ef4444",
    "grid":         "rgba(255,255,255,0.05)",
    "bg":           "#111111",
    "paper":        "#0a0a0a",
    "text":         "#a1a1aa",
    "text_bright":  "#ffffff",
}

ANOMALY_COLOUR_MAP = {
    "Z-Score Only":          COLOURS["zscore_only"],
    "Isolation Forest Only": COLOURS["iforest_only"],
    "Both Methods":          COLOURS["both"],
}


def _base_layout(title: str, height: int = 450) -> dict:
    return dict(
        title=dict(text=title, font=dict(size=13, color=COLOURS["text_bright"],
                   family="Plus Jakarta Sans, sans-serif"), x=0, xanchor="left"),
        height=height,
        paper_bgcolor=COLOURS["paper"],
        plot_bgcolor=COLOURS["bg"],
        font=dict(color=COLOURS["text"], family="JetBrains Mono, monospace", size=11),
        legend=dict(bgcolor="rgba(17,17,17,0.9)", bordercolor="rgba(255,255,255,0.07)",
                    borderwidth=1, font=dict(size=11)),
        xaxis=dict(gridcolor=COLOURS["grid"], linecolor="rgba(255,255,255,0.07)",
                   showspikes=True, spikecolor="#52525b", spikethickness=1,
                   tickfont=dict(size=10)),
        yaxis=dict(gridcolor=COLOURS["grid"], linecolor="rgba(255,255,255,0.07)",
                   tickfont=dict(size=10)),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#1a1a1a", bordercolor="rgba(255,255,255,0.1)",
                        font=dict(color="#ffffff", size=12,
                                  family="JetBrains Mono, monospace")),
        margin=dict(l=55, r=20, t=50, b=40),
    )


def plot_price_anomalies(df: pd.DataFrame, ticker: str) -> go.Figure:
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        row_heights=[0.7, 0.3], vertical_spacing=0.03)

    fig.add_trace(go.Candlestick(
        x=df.index, open=df["Open"], high=df["High"],
        low=df["Low"], close=df["Close"], name="OHLC",
        increasing_line_color="#22c55e", decreasing_line_color="#ef4444",
        showlegend=False,
    ), row=1, col=1)

    sma20 = df["Close"].rolling(20).mean()
    fig.add_trace(go.Scatter(
        x=df.index, y=sma20, name="SMA 20",
        line=dict(color="#f59e0b", width=1.5, dash="dot"),
    ), row=1, col=1)

    for atype, colour in ANOMALY_COLOUR_MAP.items():
        mask = df["Anomaly_Type"] == atype
        if mask.any():
            sub = df[mask]
            fig.add_trace(go.Scatter(
                x=sub.index, y=sub["Close"], mode="markers", name=atype,
                marker=dict(color=colour, size=9, symbol="circle-open",
                            line=dict(width=2)),
                hovertemplate=f"<b>%{{x|%Y-%m-%d}}</b><br>Close: $%{{y:.2f}}<br>Type: {atype}<extra></extra>",
            ), row=1, col=1)

    vol_colours = [COLOURS["anomaly"] if a else COLOURS["normal_vol"] for a in df["Is_Anomaly"]]
    fig.add_trace(go.Bar(
        x=df.index, y=df["Volume"], name="Volume",
        marker_color=vol_colours, opacity=0.8, showlegend=False,
        hovertemplate="<b>%{x|%Y-%m-%d}</b><br>Volume: %{y:,.0f}<extra></extra>",
    ), row=2, col=1)

    layout = _base_layout(f"{ticker} — Price & Volume", height=560)
    layout.update({
        "xaxis_rangeslider_visible": False,
        "yaxis":  dict(gridcolor=COLOURS["grid"], linecolor="rgba(255,255,255,0.07)", title="Price"),
        "yaxis2": dict(gridcolor=COLOURS["grid"], linecolor="rgba(255,255,255,0.07)", title="Volume"),
        "xaxis2": dict(gridcolor=COLOURS["grid"], linecolor="rgba(255,255,255,0.07)"),
    })
    fig.update_layout(**layout)
    return fig


def plot_zscore_heatmap(df: pd.DataFrame) -> go.Figure:
    zscore_cols   = [c for c in df.columns if c.endswith("_ZScore")]
    feature_names = [c.replace("_ZScore", "").replace("_", " ") for c in zscore_cols]
    fig = go.Figure()
    palette = [COLOURS["price"], "#22c55e", "#f59e0b"]
    for col, label, colour in zip(zscore_cols, feature_names, palette):
        fig.add_trace(go.Scatter(
            x=df.index, y=df[col], name=label,
            line=dict(color=colour, width=1.5),
            hovertemplate=f"<b>%{{x|%Y-%m-%d}}</b><br>{label}: %{{y:.2f}}<extra></extra>",
        ))
    max_z = df[zscore_cols].max().max()
    fig.add_hrect(y0=2.5, y1=max(max_z * 1.05, 3.0),
                  fillcolor="rgba(239,68,68,0.08)", line_width=0,
                  annotation_text="anomaly zone",
                  annotation_font_color=COLOURS["anomaly"])
    fig.add_hline(y=2.5, line_dash="dash", line_color=COLOURS["anomaly"],
                  line_width=1, annotation_text="threshold",
                  annotation_font_color=COLOURS["anomaly"])
    fig.update_layout(**_base_layout("Z-Score Over Time"), yaxis_title="|Z-Score|")
    return fig


def plot_iforest_scores(df: pd.DataFrame) -> go.Figure:
    colours = [COLOURS["anomaly"] if a else COLOURS["normal_vol"] for a in df["IForest_Anomaly"]]
    fig = go.Figure(go.Bar(
        x=df.index, y=df["IForest_Score"],
        marker_color=colours, opacity=0.85,
        hovertemplate="<b>%{x|%Y-%m-%d}</b><br>Score: %{y:.4f}<extra></extra>",
    ))
    fig.update_layout(**_base_layout("Isolation Forest Scores"),
                      yaxis_title="Anomaly Score", showlegend=False)
    return fig


def plot_return_distribution(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=df.loc[~df["Is_Anomaly"], "Daily_Return"],
        name="Normal", marker_color=COLOURS["price"], opacity=0.65, nbinsx=50,
    ))
    fig.add_trace(go.Histogram(
        x=df.loc[df["Is_Anomaly"], "Daily_Return"],
        name="Anomaly", marker_color=COLOURS["anomaly"], opacity=0.85, nbinsx=30,
    ))
    fig.update_layout(**_base_layout("Return Distribution"),
                      barmode="overlay", xaxis_title="Daily Return (%)", yaxis_title="Count")
    return fig


def plot_anomaly_scatter(df: pd.DataFrame) -> go.Figure:
    fig = px.scatter(
        df.reset_index(), x="Volume", y="Daily_Return", color="Anomaly_Type",
        color_discrete_map={
            "Normal":                "#1e3a5f",
            "Z-Score Only":          COLOURS["zscore_only"],
            "Isolation Forest Only": COLOURS["iforest_only"],
            "Both Methods":          COLOURS["both"],
        },
        hover_data={"Date": True, "Close": True},
        labels={"Daily_Return": "Daily Return (%)", "Volume": "Volume"},
        template="plotly_dark", opacity=0.75,
    )
    fig.update_layout(**_base_layout("Feature Space — Return vs Volume"),
                      xaxis_title="Volume", yaxis_title="Daily Return (%)")
    return fig

# ── Chart 6: Anomaly calendar heatmap ──────────────────────────────────────

def plot_calendar_heatmap(df: pd.DataFrame) -> go.Figure:
    """
    Calendar heatmap — anomaly intensity by month (rows) and day-of-month (cols).
    Each cell shows the count of anomalous days in that month/day combination.
    Gives an instant visual of which periods cluster with unusual activity.
    """
    anomalies = df[df["Is_Anomaly"]].copy()
    anomalies["month"] = anomalies.index.month
    anomalies["day"]   = anomalies.index.day

    # Pivot: rows = months, cols = days 1–31
    pivot = (
        anomalies.groupby(["month", "day"])
        .size()
        .reset_index(name="count")
        .pivot(index="month", columns="day", values="count")
        .reindex(index=range(1, 13), columns=range(1, 32))
        .fillna(0)
    )

    month_labels = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
    ]

    fig = go.Figure(
        go.Heatmap(
            z=pivot.values,
            x=list(range(1, 32)),
            y=month_labels,
            colorscale=[
                [0.0,  "#111111"],
                [0.01, "#1e3a5f"],
                [0.3,  "#2563eb"],
                [0.6,  "#3b82f6"],
                [1.0,  "#ef4444"],
            ],
            showscale=True,
            colorbar=dict(
                title=dict(text="Anomalies", font=dict(color=COLOURS["text"], size=11)),
                tickfont=dict(color=COLOURS["text"], size=10, family="JetBrains Mono"),
                bgcolor="rgba(0,0,0,0)",
                borderwidth=0,
                thickness=12,
            ),
            hovertemplate=(
                "<b>%{y} · Day %{x}</b><br>"
                "Anomalies: %{z:.0f}<extra></extra>"
            ),
            xgap=3,
            ygap=3,
        )
    )

    layout = _base_layout("Anomaly Calendar — Intensity by Month & Day", height=420)
    layout["xaxis"] = dict(
        title="Day of Month",
        tickmode="linear", tick0=1, dtick=1,
        gridcolor="rgba(0,0,0,0)",
        tickfont=dict(size=9, family="JetBrains Mono"),
        linecolor="rgba(255,255,255,0.07)",
    )
    layout["yaxis"] = dict(
        title="",
        tickfont=dict(size=11, family="JetBrains Mono"),
        gridcolor="rgba(0,0,0,0)",
        linecolor="rgba(255,255,255,0.07)",
        autorange="reversed",
    )

    fig.update_layout(**layout)
    return fig