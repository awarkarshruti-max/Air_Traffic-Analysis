import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Page title
st.title("✈️ Air Traffic Analysis Dashboard")

# Load data
df = pd.read_csv("air_traffic_data.csv")
df.columns = df.columns.str.replace(' ', '_', regex=True)

# Show dataset
st.subheader("Dataset Preview")
st.dataframe(df.head())

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("Filter Options")

# GEO Region filter
regions = st.sidebar.multiselect(
    "Select GEO Region",
    options=df["GEO_Region"].unique(),
    default=df["GEO_Region"].unique()
)

# Airline filter (if exists)
if "Operating_Airline" in df.columns:
    airlines = st.sidebar.multiselect(
        "Select Airline",
        options=df["Operating_Airline"].unique(),
        default=df["Operating_Airline"].unique()
    )
    df = df[df["Operating_Airline"].isin(airlines)]

# Apply region filter
df = df[df["GEO_Region"].isin(regions)]

# -------------------------
# Count Plot
# -------------------------
st.subheader("Distribution by Geographical Region")

fig1, ax1 = plt.subplots(figsize=(10,5))
sb.countplot(x=df["GEO_Region"], palette="hot", ax=ax1)
plt.xticks(rotation=90)
plt.xlabel("Geographical Region")
plt.ylabel("Count")
st.pyplot(fig1)

# -------------------------
# Aggregations
# -------------------------
if "Passenger_Count" in df.columns:

    t = df.groupby("Operating_Airline")["Passenger_Count"].sum().sort_values(ascending=False)
    s = df.groupby("Activity_Type")["Passenger_Count"].sum().sort_values(ascending=False)

    st.subheader("Passenger Analysis")

    col1, col2 = st.columns(2)

    # Airline-wise
    with col1:
        fig2, ax2 = plt.subplots()
        sb.barplot(x=t.index, y=t.values, palette="hot", ax=ax2)
        plt.xticks(rotation=90)
        plt.title("Passengers by Airline")
        st.pyplot(fig2)

    # Activity-wise
    with col2:
        fig3, ax3 = plt.subplots()
        sb.barplot(x=s.index, y=s.values, palette="hot", ax=ax3)
        plt.xticks(rotation=90)
        plt.title("Passengers by Activity Type")
        st.pyplot(fig3)

# -------------------------
# Extra Interactive Chart
# -------------------------
st.subheader("Custom Visualization")

x_axis = st.selectbox("Select X-axis", df.columns)
y_axis = st.selectbox("Select Y-axis", df.select_dtypes(include=['int64','float64']).columns)

fig4, ax4 = plt.subplots()
sb.barplot(x=df[x_axis], y=df[y_axis], palette="hot", ax=ax4)
plt.xticks(rotation=90)
st.pyplot(fig4)
