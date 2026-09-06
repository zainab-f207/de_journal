import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",
    user="postgres",
    password="learning123"
)
cursor = conn.cursor()

cursor.execute("INSERT INTO source_data (customer_name, amount) VALUES ('Bilal Ahmed', 60.00)")
conn.commit()

cursor.execute("SELECT MAX(created_at) FROM warehouse_data") if False else None

cursor.execute("""
    CREATE TABLE if NOT EXISTS warehouse_data (
        order_id INTEGER PRIMARY KEY,
        customer_name TEXT,
        amount NUMERIC,
        created_at TIMESTAMP Default Now(),
        load_at TIMESTAMP DEFAULT NOW()
    )
""")

cursor.execute("SELECT MAX(created_at) FROM warehouse_data")
last_loaded_at = cursor.fetchone()[0]
print(f"Last loaded timestamp: {last_loaded_at}")

if last_loaded_at is None:
    cursor.execute("SELECT order_id, customer_name, amount, created_at FROM source_data")
    print("No checkpoint found.")
else:
    cursor.execute("SELECT order_id, customer_name, amount, created_at FROM source_data WHERE created_at > %s", (last_loaded_at,))
new_rows = cursor.fetchall()
print(f"Found {len(new_rows)} new rows to load into warehouse_data")

for row in new_rows:
    cursor.execute("INSERT INTO warehouse_data (order_id, customer_name, amount, created_at) VALUES (%s, %s, %s, %s)", row)

conn.commit()
print("Incremental load completed successfully")
conn.close()