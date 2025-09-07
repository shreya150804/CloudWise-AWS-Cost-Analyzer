import pandas as pd

# --- Daily total cost ---
def daily_total(df: pd.DataFrame) -> pd.DataFrame:
    
    #Aggregate daily total spend.
    #Returns: DataFrame with columns [date, daily_cost]
    
    out = (
        df.groupby("date", as_index=False)["cost"]
        .sum()
        .rename(columns={"cost": "daily_cost"})
    )
    return out.sort_values("date").reset_index(drop=True)

# --- Fill missing days ---
def fill_missing_daily(daily_df: pd.DataFrame) -> pd.DataFrame:
    
    #Ensure there is a row for each date, fill missing costs with 0.
    
    full_idx = pd.date_range(
        start=daily_df["date"].min(),
        end=daily_df["date"].max(),
        freq="D"
    )
    out = daily_df.set_index("date").reindex(full_idx).rename_axis("date").reset_index()
    out["daily_cost"] = out["daily_cost"].fillna(0.0)
    return out


# --- Service-level breakdown ---
def service_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    
    #Total cost per service across the period.
    
    return (
        df.groupby("service", as_index=False)["cost"].sum().sort_values("cost", ascending=False).reset_index(drop=True)
    )


# --- Region-level breakdown ---
def region_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    
    #Total cost per region across the period.
    
    return (
        df.groupby("region", as_index=False)["cost"]
        .sum()
        .sort_values("cost", ascending=False)
        .reset_index(drop=True)
    )

def monthly_total(df: pd.DataFrame) -> pd.DataFrame:
    
    #Monthly aggregated spend.
    
    s = (
        df.set_index("date")["cost"]
        .resample("MS")
        .sum()
        .rename("monthly_cost")
        .reset_index()
    )
    return s


# Pivot (date × service) 
def pivot_service_by_date(df: pd.DataFrame) -> pd.DataFrame:
    
    #Pivot: rows=date, columns=service, values=cost.
    
    p = pd.pivot_table(
        df,
        index="date",
        columns="service",
        values="cost",
        aggfunc="sum",
        fill_value=0.0
    )
    return p.sort_index()


def percent_contribution_per_day(df: pd.DataFrame) -> pd.DataFrame:
    
    #For each (date, service), computing % of service cost in total daily spend.
    
    daily_service = df.groupby(["date", "service"], as_index=False)["cost"].sum()
    total_per_day = daily_service.groupby("date")["cost"].transform("sum")
    daily_service["pct_of_day"] = (daily_service["cost"] / total_per_day).fillna(0.0)
    return daily_service.sort_values(["date", "pct_of_day"], ascending=[True, False])