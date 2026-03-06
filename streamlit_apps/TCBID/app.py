import streamlit as st
import pandas as pd
import plotly.express as px

file_data = pd.read_csv('report.csv')

file_data.set_index('record_id', inplace = True)

st.dataframe(file_data.head())

profit_by_country = file_data.groupby(['country','segment'],
                                      as_index=False)['profit'].sum()

st.dataframe(profit_by_country)
st.divider()

option = st.toggle('stacked')

st.bar_chart(data = profit_by_country,
             x = 'country',
             y = 'profit',
             color = 'segment',
             stack = option)

st.subheader('Map')
st.divider()
st.map(file_data,
       size = 'profit')

st.divider()

px_data = px.data.gapminder()

fig = px.scatter_geo(px_data, 
                     locations="iso_alpha",
                     color = "continent",
                     hover_name = "country",
                     size = "pop",
                     projection = "orthographic")

st.plotly_chart(fig)

fig2 = px.choropleth(px_data, 
                     locations='iso_alpha', 
                     color='gdpPercap', 
                     labels='country', 
                     animation_frame='year',
             color_continuous_scale='rainbow')

st.plotly_chart(fig2)