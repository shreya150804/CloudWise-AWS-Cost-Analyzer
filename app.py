import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.data_loader import get_data
from utils.analysis import daily_total, fill_missing_daily, service_breakdown
from utils.anomaly import detect_anomalies, anomaly_report
from utils.ai import explain_anomalies

st.set_page_config(
    page_title="CloudWise: AWS Cost Analyzer",
    layout="wide"
)

st.title("CloudWise: AWS Cost Analyzer")
st.markdown("""
Upload your AWS billing CSV or use synthetic data to detect anomalies.
Interactive charts visualize trends and highlight cost spikes.
""")

st.sidebar.header("Data Options")

data_source = st.sidebar.selectbox("Select Data Source", ["CSV", "Synthetic"])
csv_file = None
if data_source == "CSV":
    csv_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

zscore_threshold = st.sidebar.slider("Z-score Threshold", min_value=1, max_value=5, value=2)


try:
    if data_source == "CSV" and csv_file:
        df = get_data(source="csv", path=csv_file)
    else:
        df = get_data(source="synthetic")

    st.success("Data loaded successfully!")
    st.dataframe(df.head())

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()


# Aggregate daily costs
daily_df = daily_total(df)
daily_df = fill_missing_daily(daily_df)

# Detect anomalies using Z-score
anomaly_df = detect_anomalies(daily_df, threshold=zscore_threshold)

st.subheader("Daily Cost Overview")
st.dataframe(anomaly_df)


report_df = anomaly_report(anomaly_df, df)

if report_df.empty:
    st.warning("No anomalies detected. Explanation column cannot be generated.")
else:
    report_df = explain_anomalies(report_df)
    st.subheader("Anomaly Report with Explanations")
    st.dataframe(report_df)





st.subheader("Cost Trends Over Time 📈")

# # Highlight anomalies in chart
daily_df['Anomaly'] = anomaly_df['is_anomaly'].replace({True:'Yes', False:'No'})
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=daily_df['date'],
    y=daily_df['daily_cost'],
    mode='lines',
    name='Daily Cost',
    line=dict(color='lightskyblue', width=2),
    hovertemplate='Date: %{x}<br>Cost: %{y:.2f}<extra></extra>'
))

anomaly_points = daily_df[daily_df['is_anomaly'] == True]
if not anomaly_points.empty:
    fig.add_trace(go.Scatter(
        x=anomaly_points['date'],
        y=anomaly_points['daily_cost'],
        mode='markers',
        name='Anomalies',
        marker=dict(color='red', size=10, symbol='circle'),
        hovertemplate='Date: %{x}<br>Cost: %{y:.2f}<br><b>Anomaly</b><extra></extra>'
    ))
fig.update_layout(
    title="Daily Cost Trend with Anomalies",
    xaxis_title="Date",
    yaxis_title="daily_cost",
    template="plotly_dark"  # optional
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Service-wise Cost Breakdown 💰")
service_df = service_breakdown(df)
fig_bar = px.bar(service_df, x='service', y='cost', title="Total Cost by Service")
st.plotly_chart(fig_bar, use_container_width=True)
