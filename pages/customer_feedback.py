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


if sales_df.empty or customer_df.empty:

    st.title("Customer Insights")

    st.info(
        "📭 No customer data is available. "
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


st.title("Customer Insights")


with st.expander("👥 Show All Customers"):

    st.dataframe(
        customer_df,
        hide_index=True
    )


orders_per_customer = (

    full_df

    .groupby("Customer_Name")["Order_ID"]

    .nunique()

    .sort_values(
        ascending=False
    )

)


total_customers = customer_df[
    "Customer_ID"
].nunique()


repeat_customers = (
    orders_per_customer > 1
).sum()


if not orders_per_customer.empty:

    customer_with_highest_orders = (
        orders_per_customer.idxmax()
    )

    highest_order_count = (
        orders_per_customer.max()
    )

else:

    customer_with_highest_orders = "N/A"

    highest_order_count = 0


color = st.session_state.get(
    "color",
    "light"
)


col1, col2, col3 = st.columns(3)


with col1:

    kpi_card(
        color,
        "🙎‍♂️",
        "Total Customers",
        total_customers
    )


with col2:

    kpi_card(
        color,
        "🔁",
        "Repeat Customers",
        repeat_customers
    )


with col3:

    kpi_card(
        color,
        "🔥",
        "Most Frequent Customer",
        f"{customer_with_highest_orders} "
        f"({highest_order_count} orders)"
    )


st.divider()


with st.expander(
    "📊 See Customers with Their Number of Orders"
):

    st.dataframe(
        orders_per_customer,
        hide_index=False
    )

top_customers = (

    full_df

    .groupby("Customer_Name")["Sales"]

    .sum()

    .reset_index()

    .sort_values(
        "Sales",
        ascending=False
    )

    .head(10)

)


with st.expander(
    "💰 Revenue by Top 10 Customers"
):

    fig = px.bar(
        top_customers,
        x="Customer_Name",
        y="Sales",
        color="Customer_Name",
        title="Top 10 Customers by Revenue"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


customer_revenue = (

    full_df

    .groupby("Customer_Name")["Sales"]

    .sum()

    .reset_index()

    .sort_values(
        "Sales",
        ascending=False
    )

)

number_of_customers = len(
    customer_revenue
)


if number_of_customers >= 3:

    try:

        customer_revenue["Segmentation"] = pd.qcut(
            customer_revenue["Sales"],
            q=3,
            labels=[
                "Low value",
                "Regular",
                "High value"
            ],
            duplicates="drop"
        )



        if customer_revenue[
            "Segmentation"
        ].isna().all():

            raise ValueError

    except ValueError:

        customer_revenue["Segmentation"] = pd.cut(
            customer_revenue["Sales"],
            bins=3,
            labels=[
                "Low value",
                "Regular",
                "High value"
            ],
            include_lowest=True
        )

else:

    customer_revenue["Segmentation"] = "Regular"

st.divider()

st.subheader(
    "🎯 Customer Segmentation"
)


with st.expander(
    "See All Customers with Their Segments"
):

    st.dataframe(
        customer_revenue,
        hide_index=True
    )

high_value = customer_revenue[
    customer_revenue["Segmentation"]
    == "High value"
]


regular = customer_revenue[
    customer_revenue["Segmentation"]
    == "Regular"
]


low_value = customer_revenue[
    customer_revenue["Segmentation"]
    == "Low value"
]


col1, col2, col3 = st.columns(3)


with col1:

    with st.expander(
        "💎 High Value Customers"
    ):

        st.dataframe(
            high_value[
                ["Customer_Name", "Sales"]
            ],
            hide_index=True
        )


with col2:

    with st.expander(
        "👥 Regular Customers"
    ):

        st.dataframe(
            regular[
                ["Customer_Name", "Sales"]
            ],
            hide_index=True
        )


with col3:

    with st.expander(
        "📉 Low Value Customers"
    ):

        st.dataframe(
            low_value[
                ["Customer_Name", "Sales"]
            ],
            hide_index=True
        )

segment_count = (

    customer_revenue[
        "Segmentation"
    ]

    .value_counts()

    .reset_index()

)


segment_count.columns = [
    "Segmentation",
    "Customers"
]


fig = px.pie(
    segment_count,
    values="Customers",
    names="Segmentation",
    title="Customer Segmentation"
)


st.plotly_chart(
    fig,
    width="stretch"
)