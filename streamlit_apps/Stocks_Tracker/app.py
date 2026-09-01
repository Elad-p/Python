import streamlit as st
import pandas as pd

@st.cache_data()
def load_data():
    df = pd.read_excel('data/Large_File.xlsx')
    return df

df = load_data()
prod = st.selectbox('choosee product', df['Product'].unique())


st.write(df.loc[df['Product']==prod].head())
st.write(df.shape)

st.slider('pick a number', 1, 10)
st.number_input('also here', 1,10)

with st.expander('Click to see code'):
    st.code('''
    import streamlit as st
    import pandas as pd

    @st.cache_data()
    def load_data():
        df = pd.read_excel('data/Large_File.xlsx')
        return df

    df = load_data()
    prod = st.selectbox('choosee product', df['Product'].unique())
    '''
    )

a,b,c = st.tabs(['a :material/download:','b','c'])

with a:
    st.title('text')
    st.subheader('some more')