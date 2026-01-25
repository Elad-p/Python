# Imports
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.write("Files in current directory:", os.listdir("."))

# Basic Settings
st.set_page_config(layout='wide', 
                   page_title="Demo Dashboard", 
                   page_icon=":chart:")
path = 'streamlit_apps/koola_like/'

# Intro Section
st.title('Koola Like Demo Dashboard')
st.header('Intro to Streamlit')

st.image(path + 'dashboard.jpeg')

# Load Data
@st.cache_data(ttl=120)
def load_data():
    df = pd.DataFrame(pd.read_csv(path + 'report.csv'))
    return df

data = load_data()

with st.expander('Show Data'):
    rows_n = st.slider('Number of Rows', 1, 20)
    st.dataframe(data.head(rows_n),
                 hide_index=True)

# Filters Panel
st.sidebar.header("Filters")
selected_country = st.sidebar.multiselect(
    label = 'Select One or More Countries',
    options = data['country'].unique(), 
    default = data['country'].unique()
    )
selected_products = st.sidebar.multiselect(
    label = 'Select One or More Products',
    options = data['product_sold'].unique(), 
    default = data['product_sold'].unique()
    )
price_range = st.sidebar.slider(
    label = 'Select Sale Price Range',
    min_value = data.sale_price.min(), 
    max_value = data.sale_price.max(), 
    value = (20, 150)
    )

# Filter the Data
countries_filter = data.country.isin(selected_country)
products_filter = data.product_sold.isin(selected_products)
price_filter = data.sale_price.between(price_range[0], price_range[1])
filtered = data.loc[countries_filter & products_filter & price_filter]

# Display Metrics
st.divider()

st.subheader('Main Metrics')

col1, col2, col3 = st.columns(3)
col1.metric(
    'Total Sales (Millions)',
    value=filtered.sales.div(1000000).sum().round(),
    delta = 0.3,
    chart_data=data.sales.sample(20),
    chart_type='line',
    border=True
    )

col2.metric(
    'Total Profit (Millions)',
    value=filtered.profit.div(1000000).sum().round(),
    delta = 0.3,
    chart_data=data.profit.sample(20),
    chart_type='area',
    border=True
    )

col3.metric(
    'Total Costs (Millions)',
    value=filtered.cogs.div(1000000).sum().round(),
    delta = 0.3,
    chart_data=data.cogs.sample(20),
    chart_type='bar',
    border=True
    )

st.divider()

st.header('Activity Map')

st.map(filtered,
       size = 'profit')

# Data Viz
left_column, right_column = st.columns(2)

with left_column:
    st.subheader('Profit Over Time')
    profit_over_time = filtered.groupby('date')['profit'].sum()

    chart_type = st.selectbox('Select a Chart Type to Display',
                              options = ['Bar', 'line', 'area'])
    if chart_type == 'Bar':
        st.bar_chart(profit_over_time)
    elif chart_type == 'line':
        st.line_chart(profit_over_time)
    else:
        st.area_chart(profit_over_time)
        
st.bar_chart(filtered,
            x = 'date',
            y = 'units_sold',
            color = 'product_sold',
            stack=False,
            x_label='Country',
            y_label='Total Sold',
            height='stretch'
            )

with right_column:
    st.subheader("Sales By Customer")
    fig = px.pie(filtered,names = 'segment', 
                 values='sales', 
                 #color='units_sold'
                 )
    st.plotly_chart(fig)

if st.button('Click to approve'):
    st.balloons()

    st.success("We are ready to Launch! 🚀")



