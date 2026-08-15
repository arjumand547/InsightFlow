import streamlit as st
import pandas as pd
import plotly.express as px

from database_functions import (
    create_customerTable,
    create_productTable,
    create_salesTable,
    create_connection
)

from UI_customization import kpi_card


create_customerTable()
create_productTable()
create_salesTable()

con, cur = create_connection()

customer_df = pd.read_sql(
    "SELECT * FROM customers",
    con
)

product_df = pd.read_sql(
    "SELECT * FROM products",
    con
)

sales_df = pd.read_sql(
    "SELECT * FROM sales",
    con
)

con.close()


if sales_df.empty:

    st.title("Executive Dashboard")

    st.info(
        "📭 No sales data is available yet. "
        "Please upload a dataset from the Upload Dataset page."
    )

    st.stop()



full_df = pd.merge(
    customer_df,
    sales_df,
    on="Customer_ID",
    how="inner"
)

full_df = pd.merge(
    product_df,
    full_df,
    on="Product_ID",
    how="inner"
)


st.title("Executive Dashboard")


with st.expander("Show Full Table"):
    st.dataframe(
        full_df,
        hide_index=True
    )


with st.expander("Show Customer Table"):
    st.dataframe(
        customer_df,
        hide_index=True
    )


with st.expander("Show Product Table"):
    st.dataframe(
        product_df,
        hide_index=True
    )


with st.expander("Show Sales Table"):
    st.dataframe(
        sales_df,
        hide_index=True
    )


color = st.session_state.get(
    "color",
    "light"
)



total_orders = sales_df["Order_ID"].nunique()

total_products = product_df["Product_ID"].nunique()

total_customers = customer_df["Customer_ID"].nunique()


col1, col2, col3 = st.columns(3)


with col1:

    kpi_card(
        color,
        "🛒",
        "Total Orders",
        total_orders
    )


with col2:

    kpi_card(
        color,
        "📦",
        "Total Products",
        total_products
    )


with col3:

    kpi_card(
        color,
        "🙎‍♂️",
        "Total Customers",
        total_customers
    )


st.divider()



total_sales = full_df["Sales"].sum()

total_profit = full_df["Profit"].sum()

average_order_value = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)


col1, col2, col3 = st.columns(3)


with col1:

    kpi_card(
        color,
        "💸",
        "Total Sales",
        f"Rs. {total_sales / 1000:,.2f}k"
    )


with col2:

    kpi_card(
        color,
        "📈",
        "Total Profit",
        f"Rs. {total_profit / 1000:,.2f}k"
    )


with col3:

    kpi_card(
        color,
        "📊",
        "Average Order Value",
        f"Rs. {average_order_value / 1000:,.2f}k"
    )


st.divider()


full_df["Order_Date"] = pd.to_datetime(
    full_df["Order_Date"]
)

full_df["Month_Number"] = (
    full_df["Order_Date"].dt.month
)

full_df["Month_Name"] = (
    full_df["Order_Date"].dt.month_name()
)



monthly_sales = (

    full_df

    .groupby(
        ["Month_Number", "Month_Name"]
    )["Sales"]

    .sum()

    .reset_index()

    .sort_values("Month_Number")

)


with st.expander("📈 Monthly Sales"):

    fig = px.line(
        monthly_sales,
        x="Month_Name",
        y="Sales",
        markers=True,
        title="Monthly Sales"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


monthly_profit = (

    full_df

    .groupby(
        ["Month_Number", "Month_Name"]
    )["Profit"]

    .sum()

    .reset_index()

    .sort_values("Month_Number")

)


with st.expander("📈 Monthly Profit"):

    fig = px.line(
        monthly_profit,
        x="Month_Name",
        y="Profit",
        markers=True,
        title="Monthly Profit"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

sales_by_region = (

    full_df
    .groupby("Region")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)

)


with st.expander("🌍 Sales by Region"):

    fig = px.bar(
        sales_by_region,
        x="Region",
        y="Sales",
        color="Region",
        title="Sales by Region"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


profit_by_region = (

    full_df
    .groupby("Region")["Profit"]
    .sum()
    .reset_index()
    .sort_values("Profit", ascending=False)

)


with st.expander("💰 Profit by Region"):

    fig = px.bar(
        profit_by_region,
        x="Region",
        y="Profit",
        color="Region",
        title="Profit by Region"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


sales_by_category = (

    full_df
    .groupby("Category")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)

)


with st.expander("📦 Sales by Category"):

    fig = px.bar(
        sales_by_category,
        x="Category",
        y="Sales",
        color="Category",
        title="Sales by Category"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


profit_by_category = (

    full_df
    .groupby("Category")["Profit"]
    .sum()
    .reset_index()
    .sort_values("Profit", ascending=False)

)


with st.expander("💰 Profit by Category"):

    fig = px.bar(
        profit_by_category,
        x="Category",
        y="Profit",
        color="Category",
        title="Profit by Category"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )