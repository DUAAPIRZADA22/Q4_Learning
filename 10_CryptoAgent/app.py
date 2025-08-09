import streamlit as st
from main import run_crypto_agent

st.title("💰 Live Crypto Prices")

symbol = st.text_input("Enter Crypto Symbol (e.g. BTC, ETH)")

if st.button("Get Price"):
    if symbol:
        with st.spinner("Fetching live data..."):
            result = run_crypto_agent(symbol)
            st.success(result)
    else:
        st.warning("Please enter a valid crypto symbol.")