import streamlit as st
import pandas as pd

from database_functions import (
    create_connection,
    create_customerTable,
    create_productTable,
    create_salesTable
)



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

    st.title("Reports")

    st.info(
        "📭 No data is available for reporting. "
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



st.title("Reports")


filtered_df = full_df.copy()


filtered_df["Order_Date"] = pd.to_datetime(
    filtered_df["Order_Date"]
)


filtered_df["Year"] = (
    filtered_df["Order_Date"].dt.year
)


filtered_df["Month"] = (
    filtered_df["Order_Date"].dt.month_name()
)



st.subheader("🔎 Select Filters")


col1, col2, col3, col4 = st.columns(4)


with col1:

    category = st.multiselect(
        "Select Category",
        sorted(
            filtered_df["Category"]
            .dropna()
            .unique()
        )
    )


with col2:

    city = st.multiselect(
        "Select City",
        sorted(
            filtered_df["City"]
            .dropna()
            .unique()
        )
    )


with col3:

    month = st.multiselect(
        "Select Month",
        [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
        ]
    )


with col4:

    year = st.multiselect(
        "Select Year",
        sorted(
            filtered_df["Year"]
            .dropna()
            .unique()
        )
    )



if category:

    filtered_df = filtered_df[
        filtered_df["Category"].isin(category)
    ]


if city:

    filtered_df = filtered_df[
        filtered_df["City"].isin(city)
    ]


if month:

    filtered_df = filtered_df[
        filtered_df["Month"].isin(month)
    ]


if year:

    filtered_df = filtered_df[
        filtered_df["Year"].isin(year)
    ]

if filtered_df.empty:

    st.warning(
        "⚠️ No records match the selected filters."
    )

    st.stop()



customer_table = (

    filtered_df[
        [
            "Customer_ID",
            "Customer_Name",
            "City",
            "Region"
        ]
    ]

    .drop_duplicates()

)


sales_table = (

    filtered_df[
        [
            "Order_ID",
            "Order_Date",
            "Customer_ID",
            "Product_ID",
            "Sales",
            "Quantity",
            "Discount",
            "Profit"
        ]
    ]

    .drop_duplicates()

)


product_table = (

    filtered_df[
        [
            "Product_ID",
            "Product_Name",
            "Category",
            "Sub_Category"
        ]
    ]

    .drop_duplicates()

)

with st.expander("🛒 Sales Table"):

    st.dataframe(
        sales_table,
        hide_index=True
    )

    csv = (
        sales_table
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        "Download File",
        csv,
        file_name="sales_table.csv",
        mime="text/csv"
    )



with st.expander("👥 Customer Table"):

    st.dataframe(
        customer_table,
        hide_index=True
    )

    csv1 = (
        customer_table
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        "Download File",
        csv1,
        file_name="customers_table.csv",
        mime="text/csv"
    )


with st.expander("📦 Product Table"):

    st.dataframe(
        product_table,
        hide_index=True
    )

    csv2 = (
        product_table
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        "Download File",
        csv2,
        file_name="products_table.csv",
        mime="text/csv"
    )


with st.expander("📋 Full Merged Table"):

    st.dataframe(
        filtered_df,
        hide_index=True
    )

    csv3 = (
        filtered_df
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        "Download File",
        csv3,
        file_name="merged_table.csv",
        mime="text/csv"
    )


st.divider()


summary_report = pd.DataFrame({

    "Metric": [

        "Total Sales",
        "Total Profit",
        "Total Orders",
        "Total Customers",
        "Total Products"

    ],

    "Value": [

        filtered_df["Sales"].sum(),

        filtered_df["Profit"].sum(),

        filtered_df["Order_ID"].nunique(),

        filtered_df["Customer_ID"].nunique(),

        filtered_df["Product_ID"].nunique()

    ]

})


st.subheader(
    "📊 Business Summary Report"
)


st.dataframe(
    summary_report,
    width="stretch",
    hide_index=True
)


csv4 = (
    summary_report
    .to_csv(index=False)
    .encode("utf-8")
)


st.download_button(
    "Download Summary",
    csv4,
    file_name="summary_report.csv",
    mime="text/csv"
)


st.divider()

customer_report = (

    pd.pivot_table(
        filtered_df,
        index="Customer_Name",
        values=[
            "Order_ID",
            "Sales",
            "Profit"
        ],
        aggfunc={
            "Order_ID": "nunique",
            "Sales": "sum",
            "Profit": "sum"
        },
        fill_value=0
    )

    .reset_index()

    .rename(
        columns={
            "Order_ID": "Orders"
        }
    )

    .sort_values(
        "Sales",
        ascending=False
    )

)


st.subheader(
    "👥 Customer Report"
)


with st.expander("See Customer Report"):

    st.write(
        "Customers sorted by total sales."
    )

    st.dataframe(
        customer_report,
        width="stretch",
        hide_index=True
    )

    csv5 = (
        customer_report
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        "Download Report",
        csv5,
        file_name="customer_report.csv",
        mime="text/csv"
    )


st.divider()

product_report = (

    pd.pivot_table(
        filtered_df,
        index=[
            "Category",
            "Product_Name"
        ],
        values=[
            "Order_ID",
            "Sales",
            "Profit"
        ],
        aggfunc={
            "Order_ID": "nunique",
            "Sales": "sum",
            "Profit": "sum"
        },
        fill_value=0
    )

    .reset_index()

    .rename(
        columns={
            "Order_ID": "Orders"
        }
    )

    .sort_values(
        "Sales",
        ascending=False
    )

)


st.subheader(
    "📦 Product Report"
)


with st.expander("See Product Report"):

    st.write(
        "Products sorted by total sales."
    )

    st.dataframe(
        product_report,
        width="stretch",
        hide_index=True
    )

    csv6 = (
        product_report
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        "Download Report",
        csv6,
        file_name="products_report.csv",
        mime="text/csv"
    )