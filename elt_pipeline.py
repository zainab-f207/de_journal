import psycopg2
import csv
import logging

logging.basicConfig(
    filename='elt_pipeline.log',
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
    )

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",
    user="postgres",
    password="learning123"
)

cursor = conn.cursor()

print("Start load data from sample_orders.csv")
cursor.execute("DROP TABLE IF EXISTS raw_data")
cursor.execute("""
    CREATE TABLE raw_data (
        order_id INTEGER,
        customer_name TEXT,
        amount TEXT
        )
""")
logging.info("Extracting data from sample_orders.csv")

with open('sample_orders.csv', 'r') as file:
    reader = csv.DictReader(file)
    row_count = 0
    
    for row in reader:
        cursor.execute("INSERT INTO raw_data (order_id, customer_name, amount) VALUES (%s, %s, %s)",
        (row["order_id"], row["customer_name"], row["amount"]))
        row_count += 1

conn.commit()
logging.info(f"Loaded {row_count} rows into raw_data table")

print("Start transforming data")
cursor.execute("DROP TABLE IF EXISTS transformed_data")
cursor.execute("""
    CREATE TABLE transformed_data AS
    SELECT
        order_id,
        customer_name,
        amount::NUMERIC AS amount,
        CASE
            WHEN amount::NUMERIC > 100 THEN 'High order value'
            WHEN amount::NUMERIC >=20 THEN 'Medium order value'
            ELSE 'Low order value'
        END AS classification
    FROM raw_data
    WHERE amount ~ '^[0-9]+\\.?[0-9]*$'
""")
conn.commit()
logging.info("Data transformation completed successfully")

cursor.execute("SELECT * FROM transformed_data")
print("Transformed data:")
for row in cursor.fetchall():
    print(row)

conn.close()
print("ELT pipeline completed successfully")


