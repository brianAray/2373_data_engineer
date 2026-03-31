## Exercise 3

Goal: Visualizing the data you have analyzed and saved using Streamlit.

## Your Tasks:

1. **Environment Setup:** Ensure you are in your `streamlit-env` and create a new file named `sales_dashboard.py`.
2. **The Data Connection:** Use `pd.read_parquet("sales_summary_report.parquet")` to load your Spark output.
    - *Note:* Use `@st.cache_data` to ensure the dashboard stays snappy!
3. **The Sidebar Filter:** Create a `st.sidebar.selectbox` that allows the user to choose an `item_name`.
4. **The "Big Three" Metrics:** Display three `st.metric()` components at the top of the page:
    - **Total Revenue** for the selected item.
    - **Total Units Sold** for the selected item.
    - **Average Unit Price**.
5. **The Comparison Chart:** Below the metrics, use `st.bar_chart()` to show a comparison of `total_revenue` across **all** items (to give the selected item context).
6. **The Data Table:** Use `st.dataframe()` at the very bottom to show the full summary table.