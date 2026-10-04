import sqlite3
import threading
import webbrowser

import pandas as pd
from flask import Flask, render_template_string

app = Flask(__name__)

# STEP 1B
# Connect to the database
conn = sqlite3.connect("data.sqlite")


# STEP 2
# Employee number and last name
df_first_five = pd.read_sql("""
    SELECT employeeNumber, lastName
    FROM employees
""", conn)


# STEP 3
# Last name first, then employee number
df_five_reverse = pd.read_sql("""
    SELECT lastName, employeeNumber
    FROM employees
""", conn)


# STEP 4
# Rename employee number as ID
df_alias = pd.read_sql("""
    SELECT lastName, employeeNumber AS ID
    FROM employees
""", conn)


# STEP 5
# Create Executive / Not Executive roles
df_executive = pd.read_sql("""
    SELECT
        employeeNumber,
        lastName,
        jobTitle,
        CASE
            WHEN jobTitle = 'President'
                OR jobTitle = 'VP Sales'
                OR jobTitle = 'VP Marketing'
            THEN 'Executive'
            ELSE 'Not Executive'
        END AS role
    FROM employees
""", conn)


# STEP 6
# Find the length of each employee's last name
df_name_length = pd.read_sql("""
    SELECT LENGTH(lastName) AS name_length
    FROM employees
""", conn)


# STEP 7
# Get the first two letters of each job title
df_short_title = pd.read_sql("""
    SELECT SUBSTR(jobTitle, 1, 2) AS short_title
    FROM employees
""", conn)


# STEP 8
# Calculate the total amount for all orders
sum_total_price = pd.read_sql("""
    SELECT ROUND(priceEach * quantityOrdered) AS total_price
    FROM orderDetails
""", conn).sum()


# STEP 9
# Return order date, day, month and year
df_day_month_year = pd.read_sql("""
    SELECT
        orderDate,
        SUBSTR(orderDate, 9, 2) AS day,
        SUBSTR(orderDate, 6, 2) AS month,
        SUBSTR(orderDate, 1, 4) AS year
    FROM orders
""", conn)


# Close the connection
conn.close()


@app.route("/")
def index():
    results = [
        ("Employee numbers and last names", df_first_five),
        ("Last names and employee numbers", df_five_reverse),
        ("Employee IDs", df_alias),
        ("Executive roles", df_executive),
        ("Last-name lengths", df_name_length),
        ("Short job titles", df_short_title),
        ("Total order amount", sum_total_price.to_frame().T),
        ("Order dates", df_day_month_year),
    ]
    return render_template_string(
        """
        <!doctype html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>SQL Select Lab Results</title>
          <style>
            body { font: 16px/1.5 system-ui, sans-serif; margin: 2rem auto; max-width: 1100px; padding: 0 1rem; color: #20242a; }
            h1 { margin-bottom: .25rem; }
            nav { display: flex; flex-wrap: wrap; gap: .75rem; margin: 1.5rem 0; }
            nav a { color: #075985; }
            section { margin: 2rem 0; overflow-x: auto; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #d7dce2; padding: .5rem .75rem; text-align: left; }
            th { background: #eef4f8; }
            tr:nth-child(even) { background: #f8fafc; }
          </style>
        </head>
        <body>
          <h1>SQL Select Lab Results</h1>
          <p>Query results from the local SQLite database.</p>
          <nav>
            {% for title, table in results %}
              <a href="#result-{{ loop.index }}">{{ title }}</a>
            {% endfor %}
          </nav>
          {% for title, table in results %}
            <section id="result-{{ loop.index }}">
              <h2>{{ title }}</h2>
              {{ table.to_html(index=False, classes="results", border=0, escape=True)|safe }}
            </section>
          {% endfor %}
        </body>
        </html>
        """,
        results=results,
    )


if __name__ == "__main__":
    url = "http://127.0.0.1:5000"

    def open_browser():
        if not webbrowser.open_new_tab(url):
            print(f"Could not open a browser automatically. Visit {url}")

    threading.Timer(1, open_browser).start()
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)