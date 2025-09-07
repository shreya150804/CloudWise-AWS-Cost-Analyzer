import pandas as pd
import numpy as np

def detect_anomalies(daily_df: pd.DataFrame, threshold: float = 2.0) -> pd.DataFrame:
    
    #Detect anomalies in daily cost using Z-score method.
    #daily_df: DataFrame with columns ['date', 'daily_cost']
    
    # Mean & std
    mu = daily_df["daily_cost"].mean()
    sigma = daily_df["daily_cost"].std(ddof=0)

    # Z-scores
    daily_df["zscore"] = (daily_df["daily_cost"] - mu) / sigma

    # Anomaly flag
    daily_df["is_anomaly"] = daily_df["zscore"].abs() > threshold

    # Severity
    def classify(z):
        if abs(z) > 3: return "Severe"
        elif abs(z) > 2: return "Moderate"
        return "Normal"
    
    daily_df["severity"] = daily_df["zscore"].apply(classify)

    return daily_df

def anomaly_report(df: pd.DataFrame, original_df: pd.DataFrame) -> pd.DataFrame:
    
    #Generate structured anomaly report with service-level breakdown.
    
    anomalies = df[df["is_anomaly"]].copy()

    reports = []
    for _, row in anomalies.iterrows():
        date = row["date"]
        z = row["zscore"]
        severity = row["severity"]
        daily_cost = row["daily_cost"]

        # Compare against expected (mean)
        expected = df["daily_cost"].mean()

        # Service breakdown for that day
        breakdown = (
            original_df[original_df["date"] == date]
            .groupby("service")["cost"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        top_service = breakdown.iloc[0]["service"]
        top_cost = breakdown.iloc[0]["cost"]

        reports.append({
            "date": date,
            "daily_cost": daily_cost,
            "expected": round(expected, 2),
            "zscore": round(z, 2),
            "severity": severity,
            "top_service": top_service,
            "top_service_cost": top_cost
        })

    return pd.DataFrame(reports)