import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="learning123"
)

cursor = conn.cursor()
cursor.execute("SELECT version();")
print(cursor.fetchone())

conn.close()