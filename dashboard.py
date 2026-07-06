import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# --- Load dataset ---
df = pd.read_csv("Oct2011_Cleaned.csv")
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

st.title("Sales Dashboard - Oct 2011")

# --- Interactive Feature 1: Country filter ---
countries = df["Country"].unique().tolist()
remove_countries = st.multiselect("Remove countries from analysis:", countries, default=[])

filtered_df = df[~df["Country"].isin(remove_countries)]

# --- Visualization 1: Bar chart sales by country ---
st.subheader("Sales by Country")
sales_by_country = filtered_df.groupby("Country")["MonetaryValue"].sum().sort_values(ascending=False)
st.bar_chart(sales_by_country)

# --- Visualization 2: Line chart sales trend by day ---
st.subheader("Sales Trend by Day")

metric = st.selectbox("Select metric for trend line:", 
                      ["OrderCount", "Quantity", "BasketSize"])

daily_df = filtered_df.copy()
daily_df["Day"] = daily_df["InvoiceDate"].dt.date

if metric == "OrderCount":
    daily_trend = daily_df.groupby("Day")["InvoiceNo"].nunique()
elif metric == "Quantity":
    daily_trend = daily_df.groupby("Day")["Quantity"].sum()
elif metric == "BasketSize":
    daily_trend = daily_df.groupby("Day")["BasketSize"].mean()

# Format index as dd-mmm (e.g., 01-Oct)
daily_trend.index = pd.to_datetime(daily_trend.index).strftime("%d-%b")

st.line_chart(daily_trend)

# --- Visualization 3: Projected Next Month Sales Trend ---
st.subheader("Projected Next Month Sales Trend")

daily_sales = filtered_df.groupby(filtered_df["InvoiceDate"].dt.date)["MonetaryValue"].sum().reset_index()
daily_sales["Day"] = pd.to_datetime(daily_sales["InvoiceDate"])

# Train regression model
daily_sales["DayIndex"] = np.arange(len(daily_sales))
X = daily_sales[["DayIndex"]]
y = daily_sales["MonetaryValue"]

model = LinearRegression()
model.fit(X, y)

# Predict next 30 days
future_idx = np.arange(len(daily_sales), len(daily_sales)+30).reshape(-1,1)
future_dates = pd.date_range(start=daily_sales["Day"].iloc[-1] + pd.Timedelta(days=1), periods=30)
future_pred = model.predict(future_idx)

# Plot with formatted dd-mmm dates
fig, ax = plt.subplots()
ax.plot(daily_sales["Day"], y, label="Actual Sales")
ax.plot(future_dates, future_pred, color="red", linestyle="--", label="Projected Sales")
ax.set_xlabel("Date")
ax.set_ylabel("Sales (RM)")
ax.legend()
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%d-%b"))
fig.autofmt_xdate()

st.pyplot(fig)