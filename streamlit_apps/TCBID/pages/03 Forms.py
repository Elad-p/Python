import streamlit as st
import pandas as pd
import time

user_info = {
    'u_name': None,
    'u_join_date': None,
    'age': None,
    'gender': None
}

with st.form('User Info Form'):
    user_info['u_name'] = st.text_input('Fill your name')
    user_info['u_join_date'] = st.date_input('Select a date')
    user_info['age'] = st.number_input('Fill your name')
    user_info['gender'] = st.selectbox('Your Gender', ['Male', 'Female', 'Other'])
    st.form_submit_button('Send Info')

st.write(user_info)

st.divider()

@st.cache_data()

def load_data():
    df = pd.read_csv('report.csv')
    time.sleep(3)
    return df

file_data = load_data()

file_data.set_index('record_id', inplace = True)

profit_by_country = file_data.groupby(['country','segment'],
                                        as_index=False)['profit'].sum()

selected_country = st.pills('Pick a Country',
         file_data.country.unique())

st.bar_chart(data = 
             profit_by_country.query(f'country == "{selected_country}"'),
             x = 'segment',
             y = 'profit',
             color = 'segment',
             stack=False
             )

