import streamlit as st
import pandas as pd

from database_functions import (
    create_connection,
    create_customerTable,
    create_productTable,
    create_salesTable,
    validate_and_convert,
    Insert_Customers,
    Insert_Products,
    Insert_Sales,
    clear_database
)




create_customerTable()
create_productTable()
create_salesTable()


@st.cache_data
def load_uploaded_file(file):

    filename = file.name.lower()

    if filename.endswith(".csv"):

        return pd.read_csv(file)

    elif filename.endswith(".xlsx"):

        return pd.read_excel(file)

    return None



st.title("Upload Your Dataset")
st.write(
    "Upload your CSV or Excel sales dataset and "
    "store it securely in the InsightFlow database."
)

required_columns = [

    "Order_ID",
    "Order_Date",
    "Customer_Name",
    "Product_Name",
    "Category",
    "Sub_Category",
    "Region",
    "City",
    "Sales",
    "Quantity",
    "Discount",
    "Profit"

]


expected_dtypes = {

    "Order_ID": "string",
    "Order_Date": "date",
    "Customer_Name": "string",
    "Product_Name": "string",
    "Category": "string",
    "Sub_Category": "string",
    "Region": "string",
    "City": "string",
    "Sales": "float",
    "Quantity": "int",
    "Discount": "float",
    "Profit": "float"

}



with st.expander("📋 See Standard Columns"):

    st.dataframe(
        pd.DataFrame({
            "Required Column": required_columns
        }),
        hide_index=True
    )



if st.button(
    "🗑️ Delete All Previous Data",
    type="secondary"
):

    clear_database()

    st.success(
        "All previous data has been deleted. "
        "Your database is now empty."
    )

    st.rerun()
    st.success("Your Database is empty now!")



file = st.file_uploader(
    "Upload Dataset",
    type=["csv", "xlsx"]
)


if file:

    uploaded_df = load_uploaded_file(file)

    if uploaded_df is None:

        st.error(
            "Unsupported file format."
        )

        st.stop()


    st.success(
        f"File loaded successfully: `{file.name}`"
    )


    st.subheader("🔗 Match Your Columns")

    uploaded_columns = uploaded_df.columns.tolist()

    mapping = {}


    for column in required_columns:

        with st.container(border=True):

            col1, col2 = st.columns([1.5, 1])

            with col1:

                selected_column = st.selectbox(

                    f"Select Column for `{column}`",

                    ["Not available"] + uploaded_columns,

                    key=f"mapping_{column}"

                )

                mapping[column] = selected_column

            with col2:

                st.write(
                    f"InsightFlow `{column}` → "
                    f"`{selected_column}`"
                )




    if st.button(
        "✅ Validate Dataset",
        type="primary"
    ):


        selected_columns = [

            selected

            for selected in mapping.values()

            if selected != "Not available"

        ]


        if len(selected_columns) != len(
            set(selected_columns)
        ):

            st.error(
                "❌ The same uploaded column cannot "
                "be mapped to multiple fields."
            )

            st.stop()




        mandatory_columns = [

            "Order_ID",
            "Order_Date",
            "Customer_Name",
            "Product_Name",
            "Sales",
            "Quantity",
            "Profit"

        ]


        missing_required = [

            column

            for column in mandatory_columns

            if mapping[column] == "Not available"

        ]


        if missing_required:

            st.error(
                "❌ The following required fields "
                "cannot be empty:"
            )

            for column in missing_required:

                st.write(f"- `{column}`")

            st.stop()


        standard_df = pd.DataFrame(
            index=uploaded_df.index
        )


        for column, selected_column in mapping.items():

            if selected_column != "Not available":

                standard_df[column] = (
                    uploaded_df[selected_column]
                )

            else:

                dtype = expected_dtypes[column]

                if dtype == "string":

                    standard_df[column] = "Not available"

                elif dtype in ["int", "float"]:

                    standard_df[column] = 0

                elif dtype == "date":

                    standard_df[column] = pd.NaT


        standard_df, errors = validate_and_convert(
            standard_df,
            expected_dtypes
        )


        if errors:

            st.error(
                "❌ Dataset validation failed."
            )

            for error in errors:

                st.error(error)

            st.stop()


        st.success(
            "✅ Dataset successfully validated."
        )



        text_columns = [

            "Customer_Name",
            "Product_Name",
            "Category",
            "Sub_Category",
            "Region",
            "City"

        ]


        for column in text_columns:

            standard_df[column] = (
                standard_df[column]
                .astype("string")
                .str.strip()
            )
        duplicate_lines = standard_df.duplicated(
            subset=[
                "Order_ID",
                "Order_Date",
                "Product_Name"
            ],
            keep=False
        )


        if duplicate_lines.any():

            st.warning(
                "⚠️ Duplicate order lines were found. "
                "Duplicate records will not be inserted "
                "into the database."
            )


        customer_df = (

            standard_df[
                [
                    "Customer_Name",
                    "Region",
                    "City"
                ]
            ]

            .drop_duplicates(
                subset=["Customer_Name"]
            )

            .reset_index(drop=True)

        )


        product_df = (

            standard_df[
                [
                    "Product_Name",
                    "Category",
                    "Sub_Category"
                ]
            ]

            .drop_duplicates(
                subset=["Product_Name"]
            )

            .reset_index(drop=True)

        )


        Insert_Customers(customer_df)

        Insert_Products(product_df)


        con, cur = create_connection()


        customers = pd.read_sql(
            """
            SELECT
                Customer_ID,
                Customer_Name
            FROM customers
            """,
            con
        )


        products = pd.read_sql(
            """
            SELECT
                Product_ID,
                Product_Name
            FROM products
            """,
            con
        )


        con.close()


        customer_lookup = dict(
            zip(
                customers["Customer_Name"],
                customers["Customer_ID"]
            )
        )


        product_lookup = dict(
            zip(
                products["Product_Name"],
                products["Product_ID"]
            )
        )



        sales_df = standard_df.copy()


        sales_df["Customer_ID"] = (
            sales_df["Customer_Name"]
            .map(customer_lookup)
        )


        sales_df["Product_ID"] = (
            sales_df["Product_Name"]
            .map(product_lookup)
        )



        if sales_df["Customer_ID"].isna().any():

            st.error(
                "❌ Some customers could not be mapped "
                "to the database."
            )

            st.stop()


        if sales_df["Product_ID"].isna().any():

            st.error(
                "❌ Some products could not be mapped "
                "to the database."
            )

            st.stop()


        sales_df = sales_df[
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



        Insert_Sales(sales_df)


        con, cur = create_connection()


        customers = pd.read_sql(
            "SELECT * FROM customers",
            con
        )


        products = pd.read_sql(
            "SELECT * FROM products",
            con
        )


        sales = pd.read_sql(
            "SELECT * FROM sales",
            con
        )


        con.close()


        st.success(
            "🎉 Dataset successfully imported "
            "into InsightFlow!"
        )


        with st.expander("👥 Customers Table"):

            st.dataframe(
                customers,
                hide_index=True
            )


        with st.expander("📦 Products Table"):

            st.dataframe(
                products,
                hide_index=True
            )


        with st.expander("🛒 Sales Table"):

            st.dataframe(
                sales,
                hide_index=True
            )