import streamlit as st
from datetime import date
import pandas as pd
from prophet import Prophet
import plotly.graph_objs as go
import requests
from typing import Tuple

# -------------------
# CONFIG
# -------------------
st.set_page_config(page_title="Stock Prediction App", layout="wide", page_icon="📈")

st.title("📈 Stock Prediction App")
st.markdown(
    "Enter a stock ticker (e.g., `AAPL`, `GOOG`) and choose prediction years. "
    "This app fetches data from Alpha Vantage and forecasts using Prophet."
)

# -------------------
# SIDEBAR SETTINGS
# -------------------
st.sidebar.header("Settings")
selected_stock = st.sidebar.text_input("Enter stock symbol or ticker (e.g., AAPL, GOOG)").upper().strip()
n_years = st.sidebar.slider("Years of prediction:", 1, 5, 1)
period_days = n_years * 365

# -------------------
# API KEY LOADING
# -------------------
if "alpha_vantage_api_key" in st.secrets:
    API_KEY = st.secrets["alpha_vantage_api_key"]
else:
    API_KEY = "ZYTN01FZ9OMMIJ7W"

# -------------------
# DATA LOADING
# -------------------
@st.cache_data(ttl=60 * 60)
def load_data_alpha_vantage(ticker: str) -> pd.DataFrame:
    try:
        url = (
            f"https://www.alphavantage.co/query"
            f"?function=TIME_SERIES_DAILY&symbol={ticker}"
            f"&outputsize=full&apikey={API_KEY}"
        )
        r = requests.get(url)
        data = r.json()

        if "Time Series (Daily)" not in data:
            return pd.DataFrame()

        df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
        df.index = pd.to_datetime(df.index)
        df = df.rename(
            columns={
                "1. open": "Open",
                "2. high": "High",
                "3. low": "Low",
                "4. close": "Close",
                "5. volume": "Volume",
            }
        )
        df = df.apply(pd.to_numeric)
        df = df.sort_index()
        df = df.reset_index().rename(columns={"index": "Date"})
        return df
    except Exception:
        return pd.DataFrame()

def validate_for_prophet(df: pd.DataFrame) -> Tuple[bool, str]:
    if df.empty:
        return False, "No data returned from Alpha Vantage for that ticker."
    if "Close" not in df.columns or "Date" not in df.columns:
        return False, "Expected columns ('Date', 'Close') not found in the data."
    if df["Close"].dropna().shape[0] < 2:
        return False, "Not enough valid closing price rows for forecasting."
    return True, ""

# -------------------
# MAIN APP LOGIC
# -------------------
if selected_stock:
    with st.spinner("Loading data from Alpha Vantage..."):
        data = load_data_alpha_vantage(selected_stock)

    ok, msg = validate_for_prophet(data)
    if not ok:
        st.error(f"Cannot run forecast for '{selected_stock}': {msg}")
        st.stop()

    st.subheader(f"Raw data for {selected_stock}")
    st.write(data.tail(10))

    # Plot Open & Close
    st.subheader("Time Series Data")
    fig_raw = go.Figure()
    fig_raw.add_trace(go.Scatter(x=data["Date"], y=data["Open"], name="Open"))
    fig_raw.add_trace(go.Scatter(x=data["Date"], y=data["Close"], name="Close", line=dict(color="red")))
    fig_raw.update_layout(title_text=f"{selected_stock} — Open & Close", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig_raw, use_container_width=True)

    # Prepare data for Prophet
    df_train = data[["Date", "Close"]].rename(columns={"Date": "ds", "Close": "y"}).copy()
    df_train["ds"] = pd.to_datetime(df_train["ds"], errors="coerce")
    df_train["y"] = pd.to_numeric(df_train["y"], errors="coerce")
    df_train = df_train.dropna().reset_index(drop=True)

    if df_train.shape[0] < 2:
        st.error("After cleaning, there aren't enough data points for Prophet to train.")
        st.stop()

    # Prophet model
    m = Prophet()
    with st.spinner("Training forecasting model..."):
        m.fit(df_train)

    # Forecast
    future = m.make_future_dataframe(periods=period_days)
    forecast = m.predict(future)

    # Show forecast data
    st.subheader("Forecast data (tail)")
    st.write(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(10))

    # Plot actual vs predicted
    st.subheader("Forecast Chart (interactive)")
    fig_combined = go.Figure()

    fig_combined.add_trace(
        go.Scatter(
            x=df_train['ds'],
            y=df_train['y'],
            mode='lines',
            name='Actual',
            line=dict(color='red', width=2)
        )
    )

    fig_combined.add_trace(
        go.Scatter(
            x=forecast['ds'],
            y=forecast['yhat'],
            mode='lines',
            name='Predicted',
            line=dict(color='blue', width=2, dash='dot')
        )
    )

    fig_combined.update_layout(
        title=f"{selected_stock} — Actual vs Predicted",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=True
    )

    st.plotly_chart(fig_combined, use_container_width=True)

    # Forecast components
    st.subheader("Forecast Components")
    st.pyplot(m.plot_components(forecast))

else:
    st.info("Please enter a stock symbol or ticker in the sidebar to get started.")
