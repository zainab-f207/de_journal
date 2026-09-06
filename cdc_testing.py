import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",
    user="postgres",
    password="learning123"
)
cursor = conn.cursor()
print("Starting CDC testing...")

# cursor.execute("DROP TABLE IF EXISTS live_orders")
# cursor.execute("""
# CREATE TABLE live_orders (
#     order_id INTEGER PRIMARY KEY,
#     customer_name TEXT,
#     amount NUMERIC,
#     updated_at TIMESTAMP DEFAULT NOW()
# )
# """)
# cursor.execute("INSERT INTO live_orders VALUES (1, 'Ali Khan', 49.99, NOW() - INTERVAL '2 days')")
# cursor.execute("INSERT INTO live_orders VALUES (2, 'Sara Ahmed', 120.50, NOW() - INTERVAL '2 days')")
# conn.commit()
# print("Two 'existing' orders created")

# conn.close()
# cursor.execute("UPDATE live_orders SET amount = 55.00, updated_at = NOW() WHERE order_id = 1")
# print("Order 1 updated")
# conn.commit()


cursor.execute("SELECT MAX(updated_at) FROM new_warehouse_live_orders") if False else None

cursor.execute("""
CREATE TABLE if not exists new_warehouse_live_orders (
    order_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    amount NUMERIC,
    updated_at TIMESTAMP DEFAULT NOW()
)
""")


cursor.execute("SELECT MAX(updated_at) FROM new_warehouse_live_orders")
last_updated_at = cursor.fetchone()[0]

if last_updated_at is None:
    cursor.execute("SELECT order_id, customer_name, amount, updated_at FROM live_orders")
    print("No checkpoint found.")
else:
    cursor.execute("SELECT order_id, customer_name, amount, updated_at FROM live_orders WHERE updated_at > %s", (last_updated_at,))
new_rows = cursor.fetchall()
print(f"Found {len(new_rows)} rows were updated in live_orders since last checkpoint to load into new_warehouse_live_orders")

for row in new_rows:
    cursor.execute("""
    INSERT INTO new_warehouse_live_orders (order_id, customer_name, amount, updated_at)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (order_id)
    DO UPDATE SET
        customer_name = EXCLUDED.customer_name,
        amount = EXCLUDED.amount,
        updated_at = EXCLUDED.updated_at
""", row)

conn.commit()
print("CDC testing completed successfully")

cursor.execute("SELECT * FROM new_warehouse_live_orders ORDER BY order_id")
for row in cursor.fetchall():
    print(row)
conn.close()

