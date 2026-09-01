import streamlit as st

if 'counter' not in st.session_state:
    st.session_state.counter = 0

st.header('My Fancy Clicker',divider='rainbow')

st.subheader(f'Total Clicks: {st.session_state.counter}')

if st.button('Click me'):
    st.session_state.counter += 1
    st.rerun()



st.write(st.session_state)

