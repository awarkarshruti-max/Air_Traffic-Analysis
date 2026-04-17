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

# Clean column names
df.columns = df.columns.str.strip().str.replace(' ', '_')

# Debug (optional - remove later)
# st.write("Columns:", df.columns)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filter Options")

if "GEO_Region" in df.columns:
    region = st.sidebar.multiselect(
        "Select GEO Region",
        df["GEO_Region"].unique(),
        default=df["GEO_Region"].unique()
    )
    df = df[df["GEO_Region"].isin(region)]

# -----------------------------
# KPI
# -----------------------------
if "Passenger_Count" in df.columns:
    st.metric("Total Passengers", int(df["Passenger_Count"].sum()))

# -----------------------------
# 1. Countplot (Region)
# -----------------------------
if "GEO_Region" in df.columns:
    st.subheader("Distribution by Geographical Region")

    fig1, ax1 = plt.subplots(figsize=(10,5))
    sb.countplot(x=df["GEO_Region"], palette='hot', ax=ax1)
    plt.xticks(rotation=90)
    plt.xlabel("Geographical Region")
    plt.ylabel("Count")
    st.pyplot(fig1)

# -----------------------------
# 2. Aggregations (t, s)
# -----------------------------
st.subheader("Passenger Summary")

# Airline aggregation
if "Operating_Airline" in df.columns:
    t = df.groupby("Operating_Airline")["Passenger_Count"].sum().sort_values(ascending=False)
else:
    t = None

# Activity aggregation (FIXED)
if "Activity_Type" in df.columns:
    s = df.groupby("Activity_Type")["Passenger_Count"].sum().sort_values(ascending=False)
elif "Activity_Type_Code" in df.columns:
    s = df.groupby("Activity_Type_Code")["Passenger_Count"].sum().sort_values(ascending=False)
else:
    s = None

col1, col2 = st.columns(2)

with col1:
    if t is not None:
        fig2, ax2 = plt.subplots()
        sb.barplot(x=t.index, y=t.values, palette='hot', ax=ax2)
        plt.xticks(rotation=90)
        plt.title("Passengers by Airline")
        st.pyplot(fig2)

with col2:
    if s is not None:
        fig3, ax3 = plt.subplots()
        sb.barplot(x=s.index, y=s.values, palette='hot', ax=ax3)
        plt.xticks(rotation=90)
        plt.title("Passengers by Activity Type")
        st.pyplot(fig3)

# -----------------------------
# 3. Boxplot
# -----------------------------
if "Activity_Type_Code" in df.columns:
    st.subheader("Passenger Distribution by Activity Type")

    fig4, ax4 = plt.subplots(figsize=(10,5))
    sb.boxplot(x=df["Activity_Type_Code"], y=df["Passenger_Count"], palette='hot', ax=ax4)
    plt.xlabel("Activity Type Code")
    plt.ylabel("Passenger Count")
    st.pyplot(fig4)

# -----------------------------
# 4. Line Plot (Monthly Trend)
# -----------------------------
if "Month" in df.columns:
    st.subheader("Monthly Passenger Trend")

    # Sort months
    month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)
    df = df.sort_values("Month")

    fig5, ax5 = plt.subplots(figsize=(10,5))
    sb.lineplot(x=df["Month"], y=df["Passenger_Count"], ax=ax5)
    plt.xticks(rotation=90)
    st.pyplot(fig5)

# -----------------------------
# 5. Heatmap
# -----------------------------
if "Operating_Airline" in df.columns and "Month" in df.columns:
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
if "Operating_Airline" in df.columns:
    st.subheader("Passenger Count by Airline")

    fig7, ax7 = plt.subplots(figsize=(15,8))
    sb.barplot(x=df["Operating_Airline"], y=df["Passenger_Count"], palette='hot', ax=ax7)
    plt.xticks(rotation=90)
    st.pyplot(fig7)

# -----------------------------
# 7. Boarding Area vs Terminal
# -----------------------------
if "Boarding_Area" in df.columns and "Terminal" in df.columns:
    st.subheader("Boarding Area vs Terminal")

    a = df.groupby(["Boarding_Area", "Terminal"])["Passenger_Count"].sum().reset_index()

    fig8, ax8 = plt.subplots(figsize=(10,5))
    sb.barplot(x=a["Boarding_Area"], y=a["Passenger_Count"], hue=a["Terminal"], palette='hot', ax=ax8)
    plt.legend(title='Terminal', bbox_to_anchor=(1.0,1.0))
    st.pyplot(fig8)
