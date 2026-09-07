import psycopg2
conn = psycopg2.connect(host='localhost', port=5432, dbname='postgres', user='postgres', password='learning123')
cur = conn.cursor()
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
for row in cur.fetchall():
    print(row)