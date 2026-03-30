import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sensor Mission Control", layout="wide")
st.title("Real-Time Sensor Analytics")

# Load the summary data
@st.cache_data(ttl=60) # Refresh cache every minute
def load_data():
    return pd.read_parquet("data/sensor_summary.parquet")

try:
    df = load_data()
    
    # Top Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Hottest Sensor", df.iloc[0]['sensor_id'], f"{df.iloc[0]['avg_temp']:.2f}°C")
    col2.metric("Coldest Sensor", df.iloc[-1]['sensor_id'], f"{df.iloc[-1]['avg_temp']:.2f}°C")
    col3.metric("Total Rows Processed", f"{df['reading_count'].sum():,}")

    # Chart
    fig = px.bar(df, x='sensor_id', y='avg_temp', title="Average Temperature per Sensor",
                 color='avg_temp', color_continuous_scale='RdBu_r')
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.warning("Waiting for Airflow to generate the first summary file...")