import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Air Traffic Dashboard", layout="wide")

st.title("✈️ Air Traffic Analysis Dashboard")

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("air_traffic_data.csv")
df.columns = df.columns.str.replace(' ', '_', regex=True)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filter Options")

region = st.sidebar.multiselect(
    "Select GEO Region",
    df["GEO_Region"].unique(),
    default=df["GEO_Region"].unique()
)

df = df[df["GEO_Region"].isin(region)]

# -----------------------------
# KPI
# -----------------------------
st.metric("Total Passengers", int(df["Passenger_Count"].sum()))

# -----------------------------
# 1. Countplot (Region)
# -----------------------------
st.subheader("Distribution by Geographical Region")

fig1, ax1 = plt.subplots(figsize=(10,5))
sb.countplot(x=df["GEO_Region"], palette='hot', ax=ax1)
plt.xticks(rotation=90)
plt.xlabel("Geographical Region")
plt.ylabel("Count")
st.pyplot(fig1)

# -----------------------------
# 2. Aggregation (t, s)
# -----------------------------
t = df.groupby("Operating_Airline")["Passenger_Count"].sum().sort_values(ascending=False)
s = df.groupby("Activity_Type")["Passenger_Count"].sum().sort_values(ascending=False)

st.subheader("Passenger Summary")

col1, col2 = st.columns(2)

with col1:
    fig2, ax2 = plt.subplots()
    sb.barplot(x=t.index, y=t.values, palette='hot', ax=ax2)
    plt.xticks(rotation=90)
    plt.title("Passengers by Airline")
    st.pyplot(fig2)

with col2:
    fig3, ax3 = plt.subplots()
    sb.barplot(x=s.index, y=s.values, palette='hot', ax=ax3)
    plt.xticks(rotation=90)
    plt.title("Passengers by Activity Type")
    st.pyplot(fig3)

# -----------------------------
# 3. Boxplot
# -----------------------------
st.subheader("Passenger Distribution by Activity Type")

fig4, ax4 = plt.subplots(figsize=(10,5))
sb.boxplot(x=df["Activity_Type_Code"], y=df["Passenger_Count"], palette='hot', ax=ax4)
plt.xlabel("Activity Type Code")
plt.ylabel("Passenger Count")
st.pyplot(fig4)

# -----------------------------
# 4. Line Plot (Monthly Trend)
# -----------------------------
st.subheader("Monthly Passenger Trend")

# Sort months properly
month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
if "Month" in df.columns:
    df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)
    df = df.sort_values("Month")

fig5, ax5 = plt.subplots(figsize=(10,5))
sb.lineplot(x=df["Month"], y=df["Passenger_Count"], ax=ax5)
plt.xticks(rotation=90)
st.pyplot(fig5)

# -----------------------------
# 5. Heatmap
# -----------------------------
st.subheader("Heatmap Analysis")

q = df.pivot_table(
    values="Passenger_Count",
    index="Operating_Airline",
    columns="Month",
    aggfunc="sum",
    fill_value=0
)

fig6, ax6 = plt.subplots(figsize=(12,8))
sb.heatmap(q, annot=True, cmap='copper', ax=ax6)
st.pyplot(fig6)

# -----------------------------
# 6. Airline Barplot
# -----------------------------
st.subheader("Passenger Count by Airline")

fig7, ax7 = plt.subplots(figsize=(15,8))
sb.barplot(x=df["Operating_Airline"], y=df["Passenger_Count"], palette='hot', ax=ax7)
plt.xticks(rotation=90)
st.pyplot(fig7)

# -----------------------------
# 7. Boarding Area vs Terminal
# -----------------------------
st.subheader("Boarding Area vs Terminal")

a = df.groupby(["Boarding_Area", "Terminal"])["Passenger_Count"].sum().reset_index()

fig8, ax8 = plt.subplots(figsize=(10,5))
sb.barplot(x=a["Boarding_Area"], y=a["Passenger_Count"], hue=a["Terminal"], palette='hot', ax=ax8)
plt.legend(title='Terminal', bbox_to_anchor=(1.0,1.0))
st.pyplot(fig8)
