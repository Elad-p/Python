import streamlit as st
import seaborn as sns
import pandas as pd

st.title('Dataset Explorer')
st.subheader('Please choose a dataset from the sidebar')
datasets = sns.get_dataset_names()

ds = st.sidebar.radio('Choose a data set to analyze', datasets)
df = sns.load_dataset(ds)

shape = st.checkbox('Display Shape')
if shape:
    st.write(df.shape)

show_cols = st.checkbox('Display Dataset\'s Columns')
if show_cols:
    cols_text = ''.join(['- ' + col_name + '\n' for col_name in df.columns])
    st.markdown(cols_text)

cols = st.multiselect('Choose columns to display', df.columns)
num = st.number_input('How many rows do you want to see?', 1, 100, 1, 1)
rows = st.radio('Which rows do you want to see?', ['Top', 'Bottom', 'Just show me random rows'])
if rows == 'Top':
    st.dataframe(df[cols].head(num))
elif rows == 'Bottom':
    st.dataframe(df[cols].tail(num))
else:
    st.dataframe(df[cols].sample(num))

summary = st.checkbox('Display summary stats about this data')
if summary:
    st.dataframe(df.describe())

corr = st.checkbox('Show correlation matrix')
if corr:
    sns.heatmap(df.corr())
    st.pyplot()
