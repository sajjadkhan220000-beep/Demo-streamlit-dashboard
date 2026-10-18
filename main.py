"""A small Streamlit dashboard demonstrating the app rerun workflow."""

from datetime import date, timedelta
from math import cos, sin

import pandas as pd
import streamlit as st


st.set_page_config(page_title="Streamlit Charts Demo", page_icon="📊", layout="wide")

st.title("Streamlit Charts Demo")
st.write(
    "Explore a small, generated dataset and see how Streamlit widgets update "
    "the page when their values change."
)

# Sidebar widgets are evaluated on each rerun, so their current values drive the charts.
st.sidebar.header("Dashboard controls")
days_to_show = st.sidebar.slider("Days to display", min_value=7, max_value=60, value=30)
focus_metric = st.sidebar.selectbox(
    "Metric to highlight", options=["Revenue", "Orders", "Visitors"]
)

today = date.today()
dates = [today - timedelta(days=offset) for offset in range(days_to_show - 1, -1, -1)]
data = pd.DataFrame(
    {
        "Date": dates,
        "Revenue": [
            round(1200 + index * 18 + 220 * sin(index / 4), 2)
            for index in range(days_to_show)
        ],
        "Orders": [
            round(45 + index * 0.7 + 9 * cos(index / 5))
            for index in range(days_to_show)
        ],
        "Visitors": [
            round(800 + index * 11 + 110 * sin(index / 6))
            for index in range(days_to_show)
        ],
    }
)
chart_data = data.set_index("Date")
current_value = data[focus_metric].iloc[-1]
previous_value = data[focus_metric].iloc[-2]
change_percent = (current_value - previous_value) / previous_value * 100

st.subheader(f"At a glance: {focus_metric}")
metric_columns = st.columns(3)
metric_columns[0].metric(
    f"Latest {focus_metric}", f"{current_value:,.0f}", f"{change_percent:+.1f}% vs. prior day"
)
metric_columns[1].metric("Days shown", days_to_show)
metric_columns[2].metric("Average daily revenue", f"${data['Revenue'].mean():,.0f}")

st.subheader("Daily trends")
st.line_chart(chart_data[["Revenue", "Orders", "Visitors"]])

left_chart, right_chart = st.columns(2)
with left_chart:
    st.subheader("Revenue")
    st.area_chart(chart_data[["Revenue"]], color="#4c78a8")

with right_chart:
    st.subheader("Orders")
    st.bar_chart(chart_data[["Orders"]], color="#f58518")

with st.expander("How this Streamlit app works"):
    st.markdown(
        """
        1. Streamlit runs this file from top to bottom with `streamlit run main.py`.
        2. The sidebar widgets return their current values during each run.
        3. Those values shape the generated data and the charts below.
        4. Changing a widget triggers a rerun, refreshing the visible results.
        """
    )

st.subheader("Data behind the charts")
st.dataframe(data, use_container_width=True, hide_index=True)
