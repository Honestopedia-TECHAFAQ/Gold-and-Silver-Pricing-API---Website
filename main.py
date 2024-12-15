import streamlit as st
import random
import time
from datetime import datetime
import pandas as pd
import plotly.graph_objs as go

def generate_static_data():
    gold_base = 1800.00
    silver_base = 25.00
    gold_price = gold_base + random.uniform(-10, 10)
    silver_price = silver_base + random.uniform(-0.5, 0.5)
    return gold_price, silver_price

def get_price_change(current_price, last_price):
    if current_price > last_price:
        return "▲", "green"
    elif current_price < last_price:
        return "▼", "red"
    else:
        return "-", "gray"

def generate_chart_data(periods=10, freq="H"):
    times = pd.date_range(datetime.now(), periods=periods, freq=freq)
    gold_prices = [random.uniform(1800, 1850) for _ in range(periods)]
    silver_prices = [random.uniform(24.5, 25.5) for _ in range(periods)]
    return times, gold_prices, silver_prices

st.set_page_config(page_title="Gold and Silver Price Ticker", layout="centered")
st.title("Gold and Silver Price Ticker")
st.subheader(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
gold_price, silver_price = generate_static_data()
last_gold_price, last_silver_price = 1800, 25 
gold_arrow, gold_color = get_price_change(gold_price, last_gold_price)
silver_arrow, silver_color = get_price_change(silver_price, last_silver_price)

st.markdown(f"### **Gold (XAU)**: ${gold_price:.2f} {gold_arrow}", unsafe_allow_html=True)
st.markdown(f"<span style='color:{gold_color}; font-size:24px'>{gold_arrow}</span>", unsafe_allow_html=True)
st.markdown(f"### **Silver (XAG)**: ${silver_price:.2f} {silver_arrow}", unsafe_allow_html=True)
st.markdown(f"<span style='color:{silver_color}; font-size:24px'>{silver_arrow}</span>", unsafe_allow_html=True)

st.subheader("Price Movement Over Time")
period = st.selectbox("Select the time frame for price data", ["Hourly", "Daily", "Weekly"], index=0)
if period == "Hourly":
    periods = 10
    freq = "H"
elif period == "Daily":
    periods = 7
    freq = "D"
else:
    periods = 4
    freq = "W"

times, gold_prices, silver_prices = generate_chart_data(periods, freq)

trace_gold = go.Scatter(x=times, y=gold_prices, mode='lines+markers', name='Gold Price', line=dict(color='gold'))
trace_silver = go.Scatter(x=times, y=silver_prices, mode='lines+markers', name='Silver Price', line=dict(color='silver'))

layout = go.Layout(
    title='Gold and Silver Price Movement Over Time',
    xaxis=dict(title='Time'),
    yaxis=dict(title='Price in USD')
)

fig = go.Figure(data=[trace_gold, trace_silver], layout=layout)
st.plotly_chart(fig)

price_alert = st.checkbox("Enable price alert")
if price_alert:
    alert_price_gold = st.number_input("Set Gold Price Alert", min_value=1500.0, max_value=2000.0, value=1850.0)
    alert_price_silver = st.number_input("Set Silver Price Alert", min_value=20.0, max_value=50.0, value=26.0)
    if gold_price >= alert_price_gold:
        st.markdown(f"**Gold Alert**: Price has reached ${gold_price:.2f}!")
    if silver_price >= alert_price_silver:
        st.markdown(f"**Silver Alert**: Price has reached ${silver_price:.2f}!")

st.subheader("Integrate this widget into your website")
st.markdown("""
    <p>To integrate this price ticker into your website, copy the following HTML code:</p>
    <pre>&lt;script&gt; (function(d) { 
        var s = d.createElement("script"); 
        s.src = "YOUR_WIDGET_URL";
        d.body.appendChild(s); 
    })(document); &lt;/script&gt;</pre>
""", unsafe_allow_html=True)

st.markdown("### Precious Metals 101")
st.markdown("""
    Precious metals like **Gold** and **Silver** are commodities often used in investment and trading. The prices of these metals fluctuate based on various economic factors, such as inflation, market demand, and geopolitical stability. 
    - **Gold** is often considered a safe-haven investment during uncertain times.
    - **Silver** is also used in industrial applications, which affects its price.
""")

with st.spinner('Fetching live prices...'):
    time.sleep(2)
