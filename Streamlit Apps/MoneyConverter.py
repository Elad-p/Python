import streamlit as st
import json
import requests

@st.cache
def return_rate(from_coin='ILS', to_coin='USD'):
    rates = requests.get('https://api.exchangeratesapi.io/latest?base='+from_coin)
    res = json.loads(rates.text)['rates'][to_coin]
    date = json.loads(rates.text)['date']
    return [round(res,2), date]

coins = {"דולר קנדי - CAD": "CAD",
        "דולר הונג קונגי - HKD": "HKD",
        "קרונה איסלנדית - ISK": "ISK",
        "פסו פיליפיני - PHP": "PHP",
        "כתר דני - DKK": "DKK",
        "פורינט הונגרי - HUF": "HUF",
        "קרונה צ'כית - CZK": "CZK",
        "דולר אוסטרלי - AUD": "AUD",
        "לאו רומני חדש - RON": "RON",
        "קרונה שוודית - SEK": "SEK",
        "רופי אינדונזי - IDR": "IDR",
        "רופי הודי - INR": "INR",
        "ריאל ברזילאי - BRL": "BRL",
        "רובל רוסי - RUB": "RUB",
        "קונה - HRK": "HRK",
        "ין יפני - JPY": "JPY",
        "בט תאילנדי - THB": "THB",
        "פרנק שווייצרי - CHF": "CHF",
        "דולר סינגפורי - SGD": "SGD",
        "זלוטי פולני - PLN": "PLN",
        "לב בולגרי - BGN": "BGN",
        "לירה טורקית חדשה - TRY": "TRY",
        "יואן סיני - CNY": "CNY",
        "כתר נורבגי - NOK": "NOK",
        "דולר ניו זילנדי - NZD": "NZD",
        "ראנד דרום אפריקאי - ZAR": "ZAR",
        "דולר אמריקאי - USD": "USD",
        "פסו מקסיקני - MXN": "MXN",
        "שקל ישראלי - NIS": "ILS",
        "לירה שטרלינג - GBP": "GBP",
        "וון דרום קוראני - KRW": "KRW",
        "רינגיט מלזי - MYR": "MYR"}

data = return_rate()
st.title('מחשבון המרה')
st.subheader(f'{data[1]} שערי מטבע מעודכנים נכון לתאריך')

amount = st.number_input('בחרו סכום', min_value = 0, max_value = None, value = 0, step = 1)
from_coin = st.selectbox(':אני רוצה להמיר את הסכום ממטבע', list(coins))
to_coin = st.selectbox(':למטבע', list(coins))
btn = st.button('בצע המרה')
if btn:
    data = return_rate(coins[from_coin], coins[to_coin])
    st.header(round(amount*data[0],2))
    st.subheader(to_coin.split(' -')[0])