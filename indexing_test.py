import psycopg2

conn = psycopg2.connect(host="localhost", port=5432, dbname="postgres", user="postgres", password="learning123")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS big_orders")
cursor.execute("""
CREATE TABLE big_orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    amount NUMERIC
)
""")

# Insert 100,000 fake rows, spread across 1,000 fake customers
cursor.execute("""
INSERT INTO big_orders (customer_id, amount)
SELECT (random() * 1000)::int, (random() * 500)::numeric
FROM generate_series(1, 100000)
""")
conn.commit()
print("Inserted 100,000 rows")

# Check the query plan WITHOUT an index
cursor.execute("EXPLAIN ANALYZE SELECT * FROM big_orders WHERE customer_id = 5")
for row in cursor.fetchall():
    print(row)

print("--- Now adding an index ---")
cursor.execute("CREATE INDEX idx_big_orders_customer_id ON big_orders (customer_id)")
conn.commit()

# Check the query plan WITH an index
cursor.execute("EXPLAIN ANALYZE SELECT * FROM big_orders WHERE customer_id = 5")
for row in cursor.fetchall():
    print(row)

conn.close()