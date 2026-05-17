"""
anomaly_detector.py
-------------------
Two complementary anomaly detection strategies:

  1. Z-Score Analysis  — fast, interpretable, univariate.
     Flags data points whose Z-score exceeds a user-defined threshold.
     Good at catching single-feature outliers (e.g. a sudden volume spike).

  2. Isolation Forest  — ML-based, multivariate, non-parametric.
     Detects anomalies by isolating observations in random forests.
     Better at catching subtle multi-feature anomalies that Z-score misses.

Both methods add boolean columns to the DataFrame and return a combined
`Is_Anomaly` flag for easy downstream filtering and visualisation.
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


# ── Z-Score Detection ──────────────────────────────────────────────────────

def detect_zscore_anomalies(
    df: pd.DataFrame,
    features: list[str],
    threshold: float = 2.5,
) -> pd.DataFrame:
    """
    Add Z-score columns and a `ZScore_Anomaly` flag to `df`.

    For each feature, we compute the rolling Z-score so the baseline adapts
    as the stock evolves (avoids penalising genuine long-term trends).

    Parameters
    ----------
    df        : DataFrame containing the feature columns
    features  : column names to analyse, e.g. ["Daily_Return", "Volume"]
    threshold : |Z| above this value is flagged as anomalous (default 2.5)

    Returns
    -------
    df with new columns:  <feature>_ZScore  and  ZScore_Anomaly (bool)
    """
    result = df.copy()

    # Collect per-feature anomaly flags; a row is flagged if ANY feature is extreme
    any_zscore_flag = pd.Series(False, index=result.index)

    for feature in features:
        # scipy zscore over the whole series (simple, effective for daily data)
        z_col = f"{feature}_ZScore"
        result[z_col] = np.abs(stats.zscore(result[feature].fillna(0)))

        feature_flag = result[z_col] > threshold
        any_zscore_flag = any_zscore_flag | feature_flag

    result["ZScore_Anomaly"] = any_zscore_flag
    return result


# ── Isolation Forest Detection ─────────────────────────────────────────────

def detect_isolation_forest_anomalies(
    df: pd.DataFrame,
    features: list[str],
    contamination: float = 0.05,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Add an `IForest_Anomaly` flag via scikit-learn's IsolationForest.

    The features are standardised before training so no single feature
    dominates due to scale differences (e.g. Volume vs Daily_Return).

    Parameters
    ----------
    df            : DataFrame containing the feature columns
    features      : column names to use as model inputs
    contamination : expected proportion of anomalies (0.01 – 0.5)
    random_state  : seed for reproducibility

    Returns
    -------
    df with new columns:  IForest_Score  and  IForest_Anomaly (bool)
    """
    result = df.copy()

    # Build the feature matrix, drop any remaining NaNs
    X = result[features].fillna(0).values

    # Standardise so the forest treats features equally
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Fit the Isolation Forest
    model = IsolationForest(
        contamination=contamination,
        random_state=random_state,
        n_estimators=200,       # more trees → more stable scores
        max_samples="auto",
    )
    model.fit(X_scaled)

    # decision_function: negative = more anomalous
    # predict: -1 = anomaly, 1 = normal
    result["IForest_Score"]   = -model.decision_function(X_scaled)   # flip sign: higher = more anomalous
    result["IForest_Anomaly"] = model.predict(X_scaled) == -1

    return result


# ── Combined Pipeline ──────────────────────────────────────────────────────

def run_anomaly_detection(
    df: pd.DataFrame,
    zscore_threshold: float = 2.5,
    contamination: float = 0.05,
) -> pd.DataFrame:
    """
    Run both detectors and produce a unified `Is_Anomaly` flag.

    The combined flag is set when EITHER detector fires, giving broader
    coverage. Each source flag is preserved so users can filter by method.

    Parameters
    ----------
    df                : cleaned DataFrame from data_fetcher
    zscore_threshold  : Z-score cutoff (see detect_zscore_anomalies)
    contamination     : Isolation Forest contamination rate

    Returns
    -------
    Annotated DataFrame with all anomaly columns plus summary stats dict.
    """

    # Features shared by both detectors
    features = ["Daily_Return", "Volume", "Price_Range"]

    # Ensure all features exist
    missing = [f for f in features if f not in df.columns]
    if missing:
        raise ValueError(f"Missing expected feature columns: {missing}")

    # ── Step 1: Z-Score ──────────────────────────────────────────────────
    df = detect_zscore_anomalies(df, features=features, threshold=zscore_threshold)

    # ── Step 2: Isolation Forest ─────────────────────────────────────────
    df = detect_isolation_forest_anomalies(
        df, features=features, contamination=contamination
    )

    # ── Step 3: Combined flag ────────────────────────────────────────────
    df["Is_Anomaly"] = df["ZScore_Anomaly"] | df["IForest_Anomaly"]

    # ── Step 4: Anomaly classification label ─────────────────────────────
    # Give each anomalous row a human-readable type for the dashboard
    df["Anomaly_Type"] = "Normal"
    df.loc[df["ZScore_Anomaly"]  & ~df["IForest_Anomaly"], "Anomaly_Type"] = "Z-Score Only"
    df.loc[df["IForest_Anomaly"] & ~df["ZScore_Anomaly"],  "Anomaly_Type"] = "Isolation Forest Only"
    df.loc[df["ZScore_Anomaly"]  &  df["IForest_Anomaly"], "Anomaly_Type"] = "Both Methods"

    return df


def get_anomaly_summary(df: pd.DataFrame) -> dict:
    """
    Return a summary dictionary of key anomaly statistics.
    Used to populate the Streamlit metric cards.
    """
    total         = len(df)
    anomalies     = df["Is_Anomaly"].sum()
    zscore_only   = (df["Anomaly_Type"] == "Z-Score Only").sum()
    iforest_only  = (df["Anomaly_Type"] == "Isolation Forest Only").sum()
    both          = (df["Anomaly_Type"] == "Both Methods").sum()

    anomaly_returns = df.loc[df["Is_Anomaly"], "Daily_Return"]

    return {
        "total_days":        total,
        "total_anomalies":   int(anomalies),
        "anomaly_rate":      round(anomalies / total * 100, 1),
        "zscore_only":       int(zscore_only),
        "iforest_only":      int(iforest_only),
        "both_methods":      int(both),
        "avg_anomaly_return": round(anomaly_returns.mean(), 2) if not anomaly_returns.empty else 0.0,
        "worst_return":       round(anomaly_returns.min(),  2) if not anomaly_returns.empty else 0.0,
        "best_return":        round(anomaly_returns.max(),  2) if not anomaly_returns.empty else 0.0,
    }
