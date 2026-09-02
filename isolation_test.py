import psycopg2

con_a = psycopg2.connect(
    host="localhost", port=5432, dbname="postgres",
    user="postgres", password="learning123"
)
con_b = psycopg2.connect(
    host="localhost", port=5432, dbname="postgres",
    user="postgres", password="learning123"
)

cursor_a = con_a.cursor()
cursor_b = con_b.cursor()
cursor_b.execute("Update accounts set balance = balance - 100 where account_id = 1")
print("Transaction B: Updated account 1 balance by -100, but not committed yet.")

cursor_a.execute("SELECT * FROM accounts where account_id = 1" )
print("Transaction A: Fetched updated balance for account 1:", cursor_a.fetchone())

con_b.rollback()
print("Transaction B: Rolled back the transaction.")

