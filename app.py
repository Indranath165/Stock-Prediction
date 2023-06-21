import streamlit as st
from datetime import date

import yfinance as yf
from prophet import Prophet
import pandas as pd
from prophet.plot import plot_plotly
import plotly.graph_objs as go

# Set page configuration
st.set_page_config(page_title="Stock Prediction App", layout="wide")

# Title and sidebar
st.title("Stock Prediction App")
st.sidebar.header("Settings")

# Stock selection and years of prediction
selected_stock = st.sidebar.text_input("Enter stock symbol or ticker (e.g., AAPL, GOOG)")

if selected_stock:
    n_years = st.sidebar.slider("Years of prediction:", 1, 4)
    period = n_years * 365

    # Load data
    @st.cache_data
    def load_data(ticker):
        data = yf.download(ticker, start="2015-01-01", end=date.today().strftime("%Y-%m-%d"))
        data.reset_index(inplace=True)
        return data

    data_load_state = st.sidebar.text("Loading data...")
    data = load_data(selected_stock)
    data_load_state.text("Loading data...done!")

    # Display raw data
    st.subheader('Raw data')
    st.write(data.tail())

    # Plot raw data
    st.subheader('Time Series Data')
    fig_raw = go.Figure()
    fig_raw.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='Stock Open'))
    fig_raw.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Stock Close', line=dict(color='red')))
    fig_raw.update_layout(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig_raw)

    # Forecasting
    df_train = data[['Date', 'Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    # Display forecast data
    st.subheader('Forecast data')
    st.write(forecast.tail())

    # Create custom plot_plotly function with observed and forecast lines
    def plot_plotly_custom(m, fcst, include_observed=True, color_observed='red', color_forecast='blue'):
        fig = go.Figure()

        if include_observed:
            fig.add_trace(go.Scatter(
                name='Observed',
                x=m.history['ds'],
                y=m.history['y'],
                mode='markers',
                marker=dict(color=color_observed, size=3)
            ))

        fig.add_trace(go.Scatter(
            name='Forecast',
            x=fcst['ds'],
            y=fcst['yhat'],
            mode='lines',
            line=dict(color=color_forecast)
        ))

        return fig

    # Plot forecast data with custom colors
    st.subheader('Forecast Chart')
    fig_forecast = plot_plotly_custom(m, forecast)
    fig_forecast.update_layout(xaxis_rangeslider_visible=True)
    st.plotly_chart(fig_forecast)

    # Plot forecast components
    st.subheader('Forecast Components')
    fig_components = m.plot_components(forecast)
    st.write(fig_components)
else:
    st.warning("Please enter a stock symbol or ticker.")
