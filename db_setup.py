import sqlite3

conn = sqlite3.connect("orders.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS orders")
cursor.execute("DROP TABLE IF EXISTS customers")

cursor.execute("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    city TEXT
)
""")

cursor.execute("""
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    amount REAL NOT NULL,
    classification TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
)
""")

cursor.execute("INSERT INTO customers (customer_name, city) VALUES ('Ali Khan', 'Lahore')")
cursor.execute("INSERT INTO customers (customer_name, city) VALUES ('Sara Ahmed', 'Karachi')")
cursor.execute("INSERT INTO customers (customer_name, city) VALUES ('Zainab Fayyaz', 'Lahore')")

cursor.execute("INSERT INTO orders (customer_id, amount, classification) VALUES (1, 49.99, 'Medium order value')")
cursor.execute("INSERT INTO orders (customer_id, amount, classification) VALUES (2, 120.50, 'High order value')")
cursor.execute("INSERT INTO orders (customer_id, amount, classification) VALUES (3, 15.00, 'Low order value')")
cursor.execute("INSERT INTO orders (customer_id, amount, classification) VALUES (1, 75.00, 'Medium order value')")
cursor.execute("INSERT INTO orders (customer_id, amount, classification) VALUES (99, 500.00, 'High order value')")

conn.commit()

print("---Inner JOIN example ---")
cursor.execute("""
SELECT customers.customer_name, customers.city, orders.amount, orders.classification
FROM orders
JOIN customers ON orders.customer_id = customers.customer_id
""")
for row in cursor.fetchall():
    print(row)

print("Left JOIN")
cursor.execute("""
SELECT customers.customer_name, customers.city, orders.amount, orders.classification
FROM orders
LEFT JOIN customers ON orders.customer_id = customers.customer_id
""")

result=cursor.fetchall()

for row in result:
    print(row)
cursor.execute("""
SELECT SUM(orders.amount) FROM orders LEFT JOIN customers ON orders.customer_id = customers.customer_id
""")
print("SUM of LEFT JOIN TABLE AMOUNt:" , cursor.fetchall())

cursor.execute("SELECT SUM(amount) FROM orders")
sum = cursor.fetchall()
print("Total order amount:", sum)

print("--- Subquery: orders above average ---")
cursor.execute("""
SELECT customer_id, amount
FROM orders
WHERE amount > (SELECT AVG(amount) FROM orders)
""")
for row in cursor.fetchall():
    print(row)

print("--- CTE ---")
cursor.execute("""
WITH customer_totals AS (
    SELECT customer_id, SUM(amount) AS total_spent
    FROM orders
    GROUP BY customer_id
)
SELECT customers.customer_name, customer_totals.total_spent
FROM customer_totals
JOIN customers ON customer_totals.customer_id = customers.customer_id
ORDER BY customer_totals.total_spent DESC
""")
for row in cursor.fetchall():
    print(row)

print("--- CASE ---")
cursor.execute("""
SELECT
    customer_id,
    amount,
    CASE
        WHEN amount > 100 THEN 'High order value'
        WHEN amount >= 20 THEN 'Medium order value'
        ELSE 'Low order value'
    END AS classification
FROM orders
""")
for row in cursor.fetchall():
    print(row)

print("--- Window Function ---")
cursor.execute("""
SELECT
    customer_id,
    amount,
    AVG(amount) OVER () AS overall_avg,
    amount - AVG(amount) OVER () AS diff_from_avg
FROM orders
""")
for row in cursor.fetchall():
    print(row)

print("--- Window Function with Partition ---")
cursor.execute("""
SELECT
    customer_id,
    amount,
    AVG(amount) OVER (PARTITION BY customer_id) AS avg_for_this_customer
FROM orders
""")
for row in cursor.fetchall():
    print(row)

conn.close()