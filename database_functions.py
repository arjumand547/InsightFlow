import sqlite3
import pandas as pd




DB_NAME = "insightflow.db"


def create_connection():
    con = sqlite3.connect(DB_NAME)
    con.execute("PRAGMA foreign_keys = ON")
    cur = con.cursor()
    return con, cur




def create_customerTable():

    con, cur = create_connection()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            Customer_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Customer_Name TEXT NOT NULL UNIQUE,
            Region TEXT,
            City TEXT
        )
    """)

    con.commit()
    con.close()


def Insert_Customers(customer_df):

    con, cur = create_connection()

    for _, row in customer_df.iterrows():

        cur.execute("""
            INSERT OR IGNORE INTO customers (
                Customer_Name,
                Region,
                City
            )
            VALUES (?, ?, ?)
        """, (
            row["Customer_Name"],
            row["Region"],
            row["City"]
        ))

    con.commit()
    con.close()



def create_productTable():

    con, cur = create_connection()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            Product_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Product_Name TEXT NOT NULL UNIQUE,
            Category TEXT,
            Sub_Category TEXT
        )
    """)

    con.commit()
    con.close()


def Insert_Products(product_df):

    con, cur = create_connection()

    for _, row in product_df.iterrows():

        cur.execute("""
            INSERT OR IGNORE INTO products (
                Product_Name,
                Category,
                Sub_Category
            )
            VALUES (?, ?, ?)
        """, (
            row["Product_Name"],
            row["Category"],
            row["Sub_Category"]
        ))

    con.commit()
    con.close()



def create_salesTable():

    con, cur = create_connection()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (

            Order_ID TEXT NOT NULL,

            Order_Date TEXT,

            Customer_ID INTEGER NOT NULL,

            Product_ID INTEGER NOT NULL,

            Sales REAL,

            Quantity INTEGER,

            Discount REAL,

            Profit REAL,

            FOREIGN KEY (Customer_ID)
                REFERENCES customers(Customer_ID),

            FOREIGN KEY (Product_ID)
                REFERENCES products(Product_ID),

            UNIQUE (
                Order_ID,
                Product_ID,
                Order_Date
            )
        )
    """)

    con.commit()
    con.close()


def Insert_Sales(sales_df):

    con, cur = create_connection()

    for _, row in sales_df.iterrows():

        cur.execute("""
            INSERT OR IGNORE INTO sales (
                Order_ID,
                Order_Date,
                Customer_ID,
                Product_ID,
                Sales,
                Quantity,
                Discount,
                Profit
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["Order_ID"],
            str(row["Order_Date"]),
            row["Customer_ID"],
            row["Product_ID"],
            row["Sales"],
            row["Quantity"],
            row["Discount"],
            row["Profit"]
        ))

    con.commit()
    con.close()



def validate_and_convert(df, expected_dtypes):

    errors = []

    for column, dtype in expected_dtypes.items():

        if column not in df.columns:
            errors.append(
                f"❌ Required column `{column}` is missing."
            )
            continue


        if dtype == "string":

            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
            )

            empty = (
                df[column].isna()
                | (df[column].str.strip() == "")
            )

            if empty.any():

                rows = (
                    df.index[empty] + 2
                ).tolist()

                errors.append(
                    f"❌ `{column}` contains empty values "
                    f"at rows: {rows[:10]}"
                )


        elif dtype == "float":

            converted = pd.to_numeric(
                df[column],
                errors="coerce"
            )

            invalid = (
                converted.isna()
                & df[column].notna()
            )

            if invalid.any():

                rows = (
                    df.index[invalid] + 2
                ).tolist()

                errors.append(
                    f"❌ `{column}` contains invalid numeric "
                    f"values at rows: {rows[:10]}"
                )

            df[column] = converted

        elif dtype == "int":

            converted = pd.to_numeric(
                df[column],
                errors="coerce"
            )

            invalid = (
                converted.isna()
                & df[column].notna()
            )

            if invalid.any():

                rows = (
                    df.index[invalid] + 2
                ).tolist()

                errors.append(
                    f"❌ `{column}` contains invalid integer "
                    f"values at rows: {rows[:10]}"
                )

            decimal_values = (
                converted.dropna() % 1 != 0
            )

            if decimal_values.any():

                errors.append(
                    f"❌ `{column}` must contain whole numbers only."
                )

            df[column] = converted.astype("Int64")


        elif dtype == "date":

            converted = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            invalid = (
                converted.isna()
                & df[column].notna()
            )

            if invalid.any():

                rows = (
                    df.index[invalid] + 2
                ).tolist()

                errors.append(
                    f"❌ `{column}` contains invalid dates "
                    f"at rows: {rows[:10]}"
                )

            df[column] = converted

    return df, errors



def clear_database():

    con, cur = create_connection()

    try:

        cur.execute("DELETE FROM sales")

        cur.execute("DELETE FROM customers")

        cur.execute("DELETE FROM products")

        con.commit()

    except Exception:

        con.rollback()
        raise

    finally:

        con.close()