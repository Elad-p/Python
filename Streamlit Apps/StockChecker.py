import streamlit as st
import pandas as pd
import pandas_datareader as reader
import seaborn as sns

@st.cache
def fetch_stock(stock, start, end):
    return reader.DataReader(stock, 'yahoo', start, end)

sns.set_style('darkgrid')
st.title('Stock Checker')

stock = st.text_input('Enter a stock you wish to check')
cols = st.multiselect('What do you want to see?', ('High', 'Low', 'Open', 'Close', 'Volume', 'Adj Close'))
start = st.date_input('From:')
end = st.date_input('To:')

btn = st.button('Show')
if btn:
    try:
        df = fetch_stock(stock, start, end)
    except:
        st.error('Please check your stock trading symbol...')
    else:
        st.progress(10)
        sns.lineplot(data = df[cols])
        st.pyplot()