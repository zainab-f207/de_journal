from tkinter import INSERT, TRUE

import psycopg2
from psycopg2.sql import NULL

conn = psycopg2.connect(host="localhost", port=5432, dbname="postgres", user="postgres", password="learning123")
cursor = conn.cursor()



# --- Dimension: Customers ---
cursor.execute("""
CREATE TABLE if NOT EXISTS dim_customers (
    customer_key SERIAL PRIMARY KEY,
    customer_id INTEGER,
    customer_name TEXT,
    city TEXT,
    effective_date DATE,
    end_date DATE,
    is_current BOOLEAN
)
""")

# --- Dimension: Products ---
cursor.execute("""
CREATE TABLE if NOT EXISTS dim_products (
    product_key SERIAL PRIMARY KEY,
    product_id INTEGER,
    product_name TEXT,
    category TEXT
)
""")

# --- Dimension: Dates ---
cursor.execute("""
CREATE TABLE if NOT EXISTS dim_dates (
    date_key SERIAL PRIMARY KEY,
    full_date DATE,
    day_of_week TEXT,
    month TEXT,
    quarter INTEGER,
    year INTEGER,
    is_weekend BOOLEAN
)
""")

# --- Fact: Orders ---
cursor.execute("""
CREATE TABLE if NOT EXISTS fact_orders (
    order_key SERIAL PRIMARY KEY,
    customer_key INTEGER REFERENCES dim_customers(customer_key),
    product_key INTEGER REFERENCES dim_products(product_key),
    date_key INTEGER REFERENCES dim_dates(date_key),
    amount NUMERIC,
    quantity INTEGER
)
""")

conn.commit()
print("Star schema created: fact_orders + 3 dimension tables for data warehouse example.")


print("Inserting sample data into dim_customers to test Slowly Changing Dimensions...")

# cursor.execute("""
# INSERT INTO dim_customers (customer_id, customer_name, city, effective_date, end_date, is_current)
# VALUES (1, 'Ali Khan', 'Lahore', '2026-01-01', NULL, TRUE)
# """)
# conn.commit()

# print("Inserted sample data into dim_customers")

# Step 1: close out the old record
# cursor.execute("""
# UPDATE dim_customers
# SET end_date = CURRENT_DATE, is_current = FALSE
# WHERE customer_id = 1 AND is_current = TRUE
# """)
# conn.commit()

# # Step 2: insert the new current version
cursor.execute("""
INSERT INTO dim_customers (customer_id, customer_name, city, effective_date, end_date, is_current)
VALUES (1, 'Ali Khan', 'Islamabad', CURRENT_DATE, NULL, TRUE);
""")
conn.commit()

cursor.execute("""
SELECT * FROM dim_customers
""")
print("Updated customer record for Ali Khan to reflect new city.")
for row in cursor.fetchall():
    print(row)

conn.close()