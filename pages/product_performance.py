import streamlit as st
import pandas as pd
import plotly.express as px

from database_functions import (
    create_connection,
    create_customerTable,
    create_productTable,
    create_salesTable
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


if sales_df.empty or product_df.empty:

    st.title("Product Performance")

    st.info(
        "📭 No product sales data is available. "
        "Please upload a dataset first."
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




st.title("Product Performance")


with st.expander("📦 Product Table"):

    st.dataframe(
        product_df,
        hide_index=True
    )


st.divider()


product_summary = (

    full_df

    .groupby("Product_Name")

    .agg(
        total_sales=("Sales", "sum"),
        total_profit=("Profit", "sum"),
        total_orders=("Order_ID", "nunique")
    )

    .reset_index()

)

best_sales_row = product_summary.loc[
    product_summary["total_sales"].idxmax()
]

best_profit_row = product_summary.loc[
    product_summary["total_profit"].idxmax()
]


best_selling_product = (
    best_sales_row["Product_Name"]
)

best_sales = (
    best_sales_row["total_sales"]
)

best_profit_product = (
    best_profit_row["Product_Name"]
)

best_profit = (
    best_profit_row["total_profit"]
)


total_products = product_df["Product_ID"].nunique()


color = st.session_state.get(
    "color",
    "light"
)


col1, col2, col3 = st.columns(3)


with col1:

    kpi_card(
        color,
        "📦",
        "Total Products",
        total_products
    )


with col2:

    kpi_card(
        color,
        "🏆",
        "Best Selling Product",
        f"{best_selling_product} - "
        f"Rs. {best_sales / 1000:,.2f}k"
    )


with col3:

    kpi_card(
        color,
        "💰",
        "Most Profitable Product",
        f"{best_profit_product} - "
        f"Rs. {best_profit / 1000:,.2f}k"
    )


st.divider()



with st.expander("📊 View Overall Product Summary"):

    st.dataframe(
        product_summary.sort_values(
            "total_sales",
            ascending=False
        ),
        hide_index=True
    )



top_sales_product = product_summary.nlargest(
    15,
    "total_sales"
)


with st.expander("🏆 Top Selling Products"):

    fig = px.bar(
        top_sales_product,
        x="Product_Name",
        y="total_sales",
        color="Product_Name",
        title="Top 15 Selling Products"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


least_sales_product = product_summary.nsmallest(
    15,
    "total_sales"
)


with st.expander("📉 Least Selling Products"):

    fig = px.bar(
        least_sales_product,
        x="Product_Name",
        y="total_sales",
        color="Product_Name",
        title="15 Least Selling Products"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


st.divider()


profit_products = product_summary.nlargest(
    10,
    "total_profit"
)


with st.expander("💰 Top Profitable Products"):

    fig = px.bar(
        profit_products,
        x="Product_Name",
        y="total_profit",
        color="Product_Name",
        title="Top 10 Most Profitable Products"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )



treemap_data = (

    full_df

    .groupby(
        ["Category", "Product_Name"]
    )["Sales"]

    .sum()

    .reset_index()

)


with st.expander("📊 Product Sales Treemap"):

    fig = px.treemap(
        treemap_data,
        path=[
            "Category",
            "Product_Name"
        ],
        values="Sales",
        title="Product Sales by Category and Product"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )