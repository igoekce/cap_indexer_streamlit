#Input from:
#    https://medium.com/search?q=streamlit+stock
#    https://python.plainenglish.io/building-a-simple-stock-screener-using-streamlit-and-python-plotly-library-a6f04a2e40f9

import pandas as pd
import yfinance as yf
import streamlit as st
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from datetime import date

#ticker = yf.Ticker("^GDAXI")
#dax = ticker.history(period="12mo",interval="60m")

indices = ['^GDAXI', '^DJI', '^IXIC', '^GSPC', 'BTC-USD', 'ETH-USD', 'GC=F']

ticker = st.sidebar.selectbox(
    'Choose a Index',
     indices)  


st.subheader('General Stock Info') 

start = dt.datetime.today()-dt.timedelta(2 * 365)
end = dt.datetime.today()
df = yf.download(ticker,start,end)
df = df.reset_index()
df['sma'] = df['Adj Close'].rolling(200).mean()
df['ema'] = df['Adj Close'].ewm(span=200, min_periods=200).mean()

try:
    df.rename(columns={"Date": "Datetime"}, inplace=True)
except:
    pass

df['date'] = pd.DatetimeIndex(df['Datetime']).date
df['day'] = pd.DatetimeIndex(df['Datetime']).day
df['weekday'] = pd.DatetimeIndex(df['Datetime']).weekday

############################################################################

st.subheader('Stockprice plot')
fig = go.Figure(
        data=go.Scatter(x=df['Datetime'], y=df['Adj Close'])
    )
fig.update_layout(
    title={
        'text': "Stock Prices Over Past Two Years",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
st.plotly_chart(fig, use_container_width=True)

############################################################################



today = date.today()

st.subheader('Tech Indicator Info') 
st.subheader(today.strftime("%d/%m/%Y"))
indicatorInfo = {
        "Current Close": round(df['Close'].iloc[-1], 2),
        "Last Day Close": round(df['Close'].iloc[-2], 2),
        "Mean Close": round(df.Close.mean(), 2),
        "Volume (€)": round(df.Volume.mean(), 2),
        "SMA ": round(df['sma'].iloc[-1], 2),
        "EMA ": round(df['ema'].iloc[-1], 2)
    }

indicatorDF = pd.DataFrame(data=indicatorInfo, index=[0])
st.table(indicatorDF)

############################################################################

st.subheader('Higher vs. lower day close Analysis')
df['close-open_diff'] = df['Close'] - df['Open']
df_tmp = df.groupby('day')['close-open_diff'].apply(lambda x: pd.Series([(x < 0).sum(), (x >= 0).sum()])).unstack().rename(columns={0:"lower then day start", 1:"higher then day start"})
df_tmp['higher'] = df_tmp['higher then day start'] - df_tmp['lower then day start']
df_tmp.reset_index(inplace=True)

fig = go.Figure(
        data=go.Bar(x=df_tmp['day'], y=df_tmp['higher'])
    )
fig.update_layout(
    title={
        'text': "Sum of count higher vs. lower day close",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
st.plotly_chart(fig, use_container_width=True)

############################################################################

df_weekday = df.groupby('weekday')['close-open_diff'].apply(lambda x: pd.Series([(x < 0).sum(), (x >= 0).sum()])).unstack().rename(columns={0:"lower then weekday start", 1:"higher then weekday start"})
df_weekday['higher'] = df_weekday['higher then weekday start'] - df_weekday['lower then weekday start']
df_weekday.reset_index(inplace=True)

fig = go.Figure(
        data=go.Bar(x=df_weekday['weekday'], y=df_weekday['higher'])
    )
fig.update_layout(
    title={
        'text': "Sum of count higher vs. lower weekday close / 0=Monday",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
st.plotly_chart(fig, use_container_width=True)

############################################################################


############################################################################

st.subheader('DF tail plot') 
st.table(df.tail())








