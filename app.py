import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Pricing Strategy Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("C:\\dataset\\Sampledataset.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Year"] = df["Order Date"].dt.year
    return df

df = load_data()

st.title("📦 Product Pricing Strategies & Sales Performance")

# Sidebar filters
category = st.sidebar.multiselect(
    "Select Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

year = st.sidebar.selectbox(
    "Select Year",
    sorted(df["Year"].unique())
)

filtered_df = df[
    (df["Category"].isin(category)) &
    (df["Year"] == year)
]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"${filtered_df['Profit'].sum():,.0f}")
col3.metric("Avg Discount", round(filtered_df["Discount"].mean(),2))

# Sales by Sub-Category
st.subheader("Sales by Sub-Category")
fig, ax = plt.subplots()
sns.barplot(
    data=filtered_df,
    x="Sub-Category",
    y="Sales",
    estimator=sum,
    ax=ax
)
plt.xticks(rotation=45)
st.pyplot(fig)

# Discount vs Profit
st.subheader("Discount vs Profit")
fig, ax = plt.subplots()
sns.scatterplot(
    data=filtered_df,
    x="Discount",
    y="Profit",
    ax=ax
)
st.pyplot(fig)