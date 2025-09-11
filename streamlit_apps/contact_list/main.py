import streamlit as st
import pandas as pd

if "people" not in st.session_state:
    st.session_state.people = pd.DataFrame({'id': [], 'name': [], 'join_date': [], 'active': []})
    st.session_state.contacts_count = 100

st.header('Contact List', divider='rainbow')

col1, col2 = st.columns(2)
with col1.form('Add details'):
    user_name = st.text_input('Enter Contact Name')
    user_date = st.date_input('Pick Join Date')
    user_active = st.checkbox('Active User?',value=True)

    if st.form_submit_button():
        st.session_state.people.loc[len(st.session_state.people)] = [
            st.session_state.contacts_count, 
            user_name,
            user_date,
            user_active
            ]
        st.session_state.contacts_count += 1

col2.dataframe(st.session_state.people)

if st.button('Reset Table'):
    st.session_state.people = st.session_state.people.iloc[:0]
    st.session_state.contacts_count = 100
    st.rerun()

if st.button('Export Contacts'):
    st.download_button(label = 'Export Contacts', 
                       data = st.session_state.people.to_csv('Contacts_List.csv', index = False),
                       file_name = 'Contacts_List.csv')

    st.success('Contacts Exported Successfully')


