# 📈 Stock Market Anomaly Detector

An interactive dashboard that detects unusual price and volume behaviour in any stock using **Z-Score analysis** and **Isolation Forest** — powered by a live data feed from Yahoo Finance.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.33%2B-red?logo=streamlit)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4%2B-orange?logo=scikit-learn)
![License: MIT](https://img.shields.io/badge/License-MIT-green)

---

## 🖥️ Demo

> Select any ticker · choose a date range · tune the sensitivity sliders · click **Run Analysis**

The dashboard surfaces:
- Anomalous trading days overlaid on a candlestick chart
- Per-feature Z-score timelines with threshold bands
- Isolation Forest anomaly score bars
- Daily return distribution (normal vs anomalous)
- Feature-space scatter (volume × return, coloured by detection method)
- Downloadable CSV of all detected anomalies

---

## 🧠 How It Works

### Feature Engineering
Three features are derived from raw OHLCV data:

| Feature | Formula | What it captures |
|---|---|---|
| `Daily_Return` | `(Close_t / Close_{t-1} − 1) × 100` | Abnormal price moves |
| `Volume` | raw from Yahoo Finance | Abnormal trading activity |
| `Price_Range` | `(High − Low) / Open × 100` | Intraday volatility spike |

### Z-Score Analysis
Computes the absolute Z-score for each feature over the full period. Any day where **any** feature's |Z| exceeds the configured threshold (default: 2.5) is flagged.

**Strengths:** Fast, interpretable, no training required.  
**Limitation:** Univariate — each feature is evaluated independently.

### Isolation Forest
A scikit-learn `IsolationForest` is trained on all three standardised features simultaneously. Days that are easiest to "isolate" in random subspace partitions are anomalous. The `contamination` parameter controls the expected anomaly proportion.

**Strengths:** Multivariate, non-parametric, robust to high dimensionality.  
**Limitation:** Less interpretable than Z-score; sensitive to contamination setting.

### Combined Flag
A day is marked `Is_Anomaly = True` if **either** detector fires. Each anomaly is labelled:
- 🟡 **Z-Score Only** — only caught by Z-score
- 🟣 **Isolation Forest Only** — only caught by the ML model
- 🔴 **Both Methods** — highest confidence anomalies

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/stock-anomaly-detector.git
cd stock-anomaly-detector
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

The dashboard opens automatically at `http://localhost:8501`.

---

## 📁 Project Structure

```
stock-anomaly-detector/
│
├── app.py                   # Streamlit dashboard — UI and orchestration
│
├── src/
│   ├── __init__.py
│   ├── data_fetcher.py      # yfinance data retrieval & validation
│   ├── anomaly_detector.py  # Z-Score + Isolation Forest logic
│   └── visualizer.py        # Plotly chart builders
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Configuration Parameters

| Parameter | Default | Description |
|---|---|---|
| Ticker Symbol | `AAPL` | Any Yahoo Finance ticker (stocks, ETFs, crypto) |
| Start Date | 2 years ago | Historical data start |
| End Date | Today | Historical data end |
| Z-Score Threshold | `2.5` | Anomaly sensitivity (lower = more anomalies) |
| IF Contamination | `0.05` | Expected anomaly proportion (0.01 – 0.20) |

---

## 🛠️ Tech Stack

| Library | Role |
|---|---|
| `yfinance` | Live OHLCV data from Yahoo Finance |
| `pandas` / `numpy` | Data wrangling and feature engineering |
| `scipy` | Z-score computation |
| `scikit-learn` | Isolation Forest + StandardScaler |
| `plotly` | Interactive charts |
| `streamlit` | Web dashboard framework |

---

## 📌 Example Tickers to Try

| Ticker | Asset | Why it's interesting |
|---|---|---|
| `TSLA` | Tesla | High volatility → many anomalies |
| `NVDA` | NVIDIA | Dramatic AI-boom price action 2023–24 |
| `BTC-USD` | Bitcoin | Extreme crypto anomalies |
| `SPY` | S&P 500 ETF | Market-wide events (COVID crash, etc.) |
| `GME` | GameStop | Meme stock squeeze clearly visible |

---

## 🔮 Potential Extensions

- [ ] Multi-ticker comparison dashboard
- [ ] Correlation of anomalies with news events (via NewsAPI)
- [ ] LSTM-based anomaly detection for sequence modelling
- [ ] Email / Slack alerts for real-time anomaly detection
- [ ] Backtesting: does buying after anomalies outperform?

---

## 📄 License

MIT © 2024. Free to use, modify, and distribute.
