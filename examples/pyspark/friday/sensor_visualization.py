import streamlit as st
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="Sensor Monitor", layout="wide")

# 2. Data Loading
# It is really important that whenever you are loading in data
# You cache the data
# Otherwise whenever filter the data in someway using Streamlit, it will load in the data from memory again

@st.cache_data
def load_sensor_data():
    df = pd.read_parquet("output/sensor_stats.parquet")
    return df

df = load_sensor_data()

# Sidebar - Controls
with st.sidebar:
    st.title("Settings")
    st.write("Filter the dashboard vitals")

    # User Input for temperature thresholds
    temp_threshold = st.slider(
        "Min Average Temperature",
        min_value=float(df["avg_temp"].min()),
        max_value=float(df["avg_temp"].max()),
        value=20.0
    )

# Filter the data based on sidebar input
filtered_df = df[df["avg_temp"] >= temp_threshold]

# Main UI: st.title and st.metric
st.title("Sensor Health Dashboard")
st.markdown(f"Currently monitoring **{len(df)}** total sensors")

# Displaying vitals (st.metric)
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Active Sensors", len(filtered_df), delta=len(filtered_df) - len(df))
with m2:
    global_avg = round(filtered_df["avg_temp"].mean(), 2)
    st.metric("Global Avg Temp", f"{global_avg} C")
with m3:
    total_readings = filtered_df["reading_count"].sum()
    st.metric("Total Data Points", f"{total_readings:,}")

st.divider()

# Visualization: st.chart and st.dataframe

left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("Temperature Distribution")
    # Streamlit bar_chart is good for this
    st.bar_chart(filtered_df.set_index("sensor_id")["avg_temp"])

with right_col:
    st.subheader("Sensor Stats Table")
    # st.dataframe allows users to sort the Spark results directly
    st.dataframe(filtered_df, hide_index=True, use_container_width=True)

# Alert Logic
if filtered_df["avg_temp"].max() > 25.0:
    st.warning("Heat Alert: Some sensors are reporting averages above 25 degrees")

