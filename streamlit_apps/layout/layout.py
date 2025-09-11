# KPI Row
import streamlit as st
import pandas as pd
from plotly import express as px

tips = pd.read_csv('tips.csv')

kpi1, kpi2, kpi3 = st.columns(3)

avg_bill = tips["total_bill"].mean()
avg_tip  = tips["tip"].mean()
avg_rate = (tips["tip"] / tips["total_bill"]).mean()

kpi1.metric("Avg Total Bill", f"${avg_bill:0.2f}")
kpi2.metric("Avg Tip", f"${avg_tip:0.2f}")
kpi3.metric("Avg Tip Rate", f"{avg_rate*100:0.1f}%")

st.divider()

# Charts Row
c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("Total Bill Distribution")
    fig = px.histogram(tips, x="total_bill", nbins=25)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Tip Distribution")
    fig = px.histogram(tips, x="tip", nbins=25)
    st.plotly_chart(fig, use_container_width=True)

with c3:
    st.subheader("Total Bill by Day (Box)")
    fig = px.box(tips, x="day", y="total_bill")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.header('Tabs')

tab1, tab2, tab3 = st.tabs(["Overview", "Distributions", "Relationships"])

with tab1:
    st.subheader("Daily Summary")
    df = tips.assign(tip_rate=tips["tip"]/tips["total_bill"]) \
             .groupby("day", as_index=False) \
             .agg(total_bill_sum=("total_bill","sum"),
                  tip_sum=("tip","sum"),
                  tip_rate_avg=("tip_rate","mean"))
    st.dataframe(df)

with tab2:
    colA, colB = st.columns(2)
    with colA:
        st.caption("Total Bill Distribution")
        st.plotly_chart(px.histogram(tips, x="total_bill", nbins=25), use_container_width=True, key = 111)
    with colB:
        st.caption("Tip Distribution")
        st.plotly_chart(px.histogram(tips, x="tip", nbins=25), use_container_width=True, key = 222)

with tab3:
    st.caption("Total Bill vs Tip")
    fig = px.scatter(
        tips, x="total_bill", y="tip",
        color="gender", size="size",
        hover_data=["day","time"]
    )
    st.plotly_chart(fig, use_container_width=True, key =333)

st.divider()

st.header('Expander')

with st.expander("Advanced Filters", expanded=False):
    days = st.multiselect("Days", options=tips["day"].unique().tolist(),
                          default=tips["day"].unique().tolist())
    time_choice = st.radio("Time", options=tips["time"].unique().tolist())
    min_b, max_b = float(tips["total_bill"].min()), float(tips["total_bill"].max())
    bill_range = st.slider("Total Bill Range", min_b, max_b, (min_b, max_b))

# Apply filters
flt = tips[
    tips["day"].isin(days) &
    (tips["time"] == time_choice) &
    tips["total_bill"].between(bill_range[0], bill_range[1])
]

st.write(f"Filtered rows: **{len(flt)}**")

t1, t2 = st.tabs(["Overview", "Plot"])

with t1:
    st.dataframe(flt)

with t2:
    st.plotly_chart(
        px.scatter(flt, x="total_bill", y="tip", color="gender", size="size",
                   title="Filtered: Total Bill vs Tip"),
        use_container_width=True
    )
