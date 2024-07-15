import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.express as px
import yfinance as yf
from streamlit_autorefresh import st_autorefresh

# Remove the while True loop to prevent continuous rerunning
st_autorefresh(interval=60000, key='data_refresh')

# Title
st.title("Stock Market Display")


# Search input
ticker_symbol = st.text_input("Enter a stock ticker symbol (e.g., 'MSFT'):")

# Layout: 3 columns
col1, col2, col3 = st.columns([1, 0.1, 2])  # Adjust the width ratios as needed

# Portfolio information in the first column
with col1:
    st.metric(label="Portfolio Returns", value="10%")

if ticker_symbol:
    # Attempt to fetch data for the entered ticker
    ticker_data = yf.Ticker(ticker_symbol)
    ticker_df = ticker_data.history(period="1y")  # Fetch data for the past year

    if not ticker_df.empty:
        # Plot the closing prices using Plotly Express
        fig = px.line(ticker_df, x=ticker_df.index, y="Close", title=f'{ticker_symbol.upper()} Closing Prices Over Time')
        # Display the graph
        st.plotly_chart(fig)
    else:
        # Display an error message if the data is empty (indicating an invalid ticker)
        st.error("Could not find data for the entered ticker symbol. Please try another one.")

        # First row of buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button('Show Dividends'):
            dividends = ticker_data.dividends
            st.write(dividends)

    with col2:
        if st.button('Show Splits'):
            splits = ticker_data.splits
            st.write(splits)

    with col3:
        if st.button('Show Income Statement'):
            income_stmt = ticker_data.financials
            st.write(income_stmt)

    with col4:
        if st.button('Show Balance Sheet'):
            balance_sheet = ticker_data.balance_sheet
            st.write(balance_sheet)

    # Second row of buttons (example placeholders for additional buttons)
