import random

def explain_anomaly(service, date, cost, z_score, usage_type='general'):
    explanations = [
        f"High {usage_type} usage in {service} caused the cost spike on {date}.",
        f"{service} cost increased on {date} due to unexpected {usage_type} activity.",
        f"Billing anomaly for {service} on {date} likely caused by excessive {usage_type} usage.",
        f"Temporary surge in {usage_type} for {service} led to higher charges on {date}.",
        f"Unplanned {usage_type} usage in {service} resulted in the cost spike on {date}."
    ]
    return random.choice(explanations)

def explain_anomalies(anomalies_df):
    
    anomalies_df = anomalies_df.copy()
    anomalies_df['Explanation'] = anomalies_df.apply(
        lambda row: explain_anomaly(
            service=row['top_service'],
            date=row['date'],
            cost=row['top_service_cost'],
            z_score=row['zscore'],
            usage_type=row.get('UsageType', 'general')
        ),
        axis=1
    )
    return anomalies_df
