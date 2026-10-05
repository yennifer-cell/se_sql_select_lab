# STEP 1A
# Import SQL Library and Pandas
import sqlite3

import pandas as pd

# STEP 1B
# Connect to the database
conn = sqlite3.connect("data.sqlite")

# STEP 2
# Replace None with your code
df_first_five = pd.read_sql(
    """
    SELECT employeeNumber, lastName
    FROM employees
    ORDER BY employeeNumber ASC
    """,
    conn,
)

# STEP 3
df_five_reverse = pd.read_sql(
    """
    SELECT lastName, employeeNumber
    FROM employees
    ORDER BY employeeNumber DESC
    """,
    conn,
)

# STEP 4
# Replace None with your code
df_alias = pd.read_sql(
    """
    SELECT employeeNumber AS ID, lastName, firstName, extension, email,
           officeCode, reportsTo, jobTitle
    FROM employees
    ORDER BY ID DESC
    """,
    conn,
)

# STEP 5
# Replace None with your code
df_executive = pd.read_sql(
    """
    SELECT
        employeeNumber,
        jobTitle,
        CASE
            WHEN jobTitle IN ('President', 'VP Sales', 'VP Marketing')
                THEN 'Executive'
            ELSE 'Not Executive'
        END AS role
    FROM employees
    """,
    conn,
)

# STEP 6
# Replace None with your code
df_name_length = pd.read_sql(
    """
    SELECT LENGTH(lastName) AS name_length
    FROM employees
    """,
    conn,
)

# STEP 7
# Replace None with your code
df_short_title = pd.read_sql(
    """
    SELECT SUBSTR(jobTitle, 1, 2) AS short_title
    FROM employees
    """,
    conn,
)

# STEP 8
# Replace None with your code
subtotal = pd.read_sql_query(
    """
    SELECT ROUND(priceEach * quantityOrdered, 0) AS total_price
    FROM orderDetails
    """,
    conn,
)["total_price"].sum()
sum_total_price = pd.Series([subtotal])

# STEP 9
# Replace None with your code
df_day_month_year = pd.read_sql(
    """
    SELECT
        orderDate,
        strftime('%d', orderDate) AS day,
        strftime('%m', orderDate) AS month,
        strftime('%Y', orderDate) AS year
    FROM orders
    """,
    conn,
)

# Close the connection
conn.close()
