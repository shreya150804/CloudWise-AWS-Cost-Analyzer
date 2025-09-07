import pandas as pd
import numpy as np
from datetime import datetime

def load_billing_csv(path: str) -> pd.DataFrame:
    
    #Load AWS billing CSV file.
    #Expected columns: Date, Service, Region, UsageType, Cost
    
    df = pd.read_csv(path, parse_dates=["Date"])
    df.columns = df.columns.str.strip().str.lower()
    df.columns = df.columns.str.lower()

    
    
    df["cost"] = pd.to_numeric(df["cost"], errors="coerce").fillna(0)
    
    
    df["service"] = df["service"].str.strip()
    df["region"] = df["region"].str.strip()
    
    
    return df


#-----------------------------------------------------------------------------------------------------


def generate_synthetic_data(start_date="2025-06-01", end_date="2025-08-31") -> pd.DataFrame:
    
    #Generate mock AWS billing data for testing.
    #Covers multiple services, regions, and usage types.
    
    np.random.seed(42)
    
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    services = ["EC2", "S3", "Lambda", "RDS", "CloudFront", "DynamoDB"]
    regions = ["us-east-1", "us-west-2", "ap-south-1", "eu-central-1"]
    usage_types = ["Compute", "Storage", "DataTransfer", "Requests"]

    data = []
    for date in dates:
        for service in services:
            for region in np.random.choice(regions, size=2, replace=False):
                usage_type = np.random.choice(usage_types)
                base_cost = {
                    "EC2": 20, "S3": 10, "Lambda": 5, "RDS": 15, "CloudFront": 8, "DynamoDB": 12
                }[service]
                cost = round(base_cost + np.random.normal(0, base_cost * 0.3), 2)
                cost = abs(cost)  # no negatives
                data.append([date, service, region, usage_type, cost])

    df = pd.DataFrame(data, columns=["date", "service", "region", "usageType", "cost"])
    return df

#-----------------------------------------------------------------------------------------------------


def get_data(source="csv", path=None) -> pd.DataFrame:
    
    #Get billing data from either CSV or synthetic generator.
    
    if source == "csv" and path:
        return load_billing_csv(path)
    elif source == "synthetic":
        return generate_synthetic_data()
    else:
        raise ValueError("Invalid source. Use 'csv' with path or 'synthetic'.")