import streamlit as st

if 'counter' not in st.session_state:
    st.session_state.counter = 0

st.write('Current Value', st.session_state.counter)

if st.button('Click me'):
    st.session_state.counter += 1

if st.button('Reset'):
    st.session_state.counter = 0

st.write('Counter Value: ', st.session_state.counter)

x = {'a':1,
     'b': 2}

st.write(x.b)