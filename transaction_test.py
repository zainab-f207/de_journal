import psycopg2

conn = psycopg2.connect(
    host="localhost", port=5432, dbname="postgres",
    user="postgres", password="learning123"
)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS accounts")
cursor.execute("""
CREATE TABLE accounts (
    account_id INTEGER PRIMARY KEY,
    owner_name TEXT NOT NULL,
    balance NUMERIC NOT NULL
)
""")
cursor.execute("INSERT INTO accounts VALUES (1, 'Ali', 500)")
cursor.execute("INSERT INTO accounts VALUES (2, 'Sara', 200)")
conn.commit()

# Simulate a transfer that fails partway through
try:
    cursor.execute("UPDATE accounts SET balance = balance - 100 WHERE account_id = 1")
    cursor.execute("UPDATE accounts SET balance = balance + 100 WHERE account_id = 99")  # 99 doesn't exist, but this won't error by itself
    raise Exception("Simulated crash mid-transfer!")
    conn.commit()
except Exception as e:
    print("Error occurred:", e)
    conn.rollback()
    print("Transaction rolled back")

cursor.execute("SELECT * FROM accounts")
for row in cursor.fetchall():
    print(row)

conn.close()