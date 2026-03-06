import streamlit as st
import pandas as pd

st.set_page_config(
    layout='wide'
)

col_a, col_b = st.columns(2)
col_b.image('dashboard.jpeg')

col_a.write('This is some explanation text')

col1, col2, col3 = st.columns(3)

col2.image('streamlit_apps/TCBID/dashboard.jpeg')

col_a, col_b = st.columns([1,2])
col_b.image('streamlit_apps/TCBID/dashboard.jpeg')

col_a.write('This is some explanation text')

name_field = st.container()

age_field = st.container()

u_name = name_field.text_input('Enter your name')

u_age = age_field.number_input('Enter your age',
                min_value=5,
                max_value=120,
                step=1,
                value=None)

if st.button('Send info'):
    if not u_name:
        name_field.error('You have to fill your name')
    elif not u_age:
        age_field.error('You forgot to fill your age')
    else:
        st.success('Thank you!')


name_field.metric('Total Sales',100)

st.button('press me', key = 'btn1')
st.button('press me', key = 'btn2')

info = {
    'name': 'elad',
    'age': 30
}

a,b = st.columns(2)

name = a.text_input('name')

if name:
    b.number_input('age', value=info['age'])

st.divider()
t1, t2, t3 = st.tabs(['Chart', 'Data', 'tab3'])


with t1:
    file_data = pd.read_csv('streamlit_apps/TCBID/report.csv')

    file_data.set_index('record_id', inplace = True)

    profit_by_country = file_data.groupby(['country','segment'],
                                        as_index=False)['profit'].sum()

    st.bar_chart(data = profit_by_country,
             x = 'country',
             y = 'profit',
             color = 'segment',
             )
    
with t2:
     st.dataframe(file_data.head())

st.divider()

st.bar_chart(data = profit_by_country,
             x = 'country',
             y = 'profit',
             color = 'segment',
             stack=False
             )

with st.expander('Click to view the data'):
    st.dataframe(file_data.head())

selected_country = st.pills('Pick a Country',
         file_data.country.unique())

st.bar_chart(data = 
             profit_by_country.query(f'country == "{selected_country}"'),
             x = 'segment',
             y = 'profit',
             color = 'segment',
             stack=False
             )

price_range = st.slider('Please pick a range',
          min_value=1,
          max_value=100,
          value = (50,70))
st.write(price_range)

# df.loc[df.price.between(price_range[0], price_range[1])]


st.multiselect('Pick one or more', ['One', 'Two', 'Three'])
