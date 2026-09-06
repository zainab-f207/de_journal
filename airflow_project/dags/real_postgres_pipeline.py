from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import psycopg2

def extract_and_load(**context):
    conn = psycopg2.connect(
        host="de_postgres",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="learning123"
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS airflow_orders (
            order_id INTEGER PRIMARY KEY,
            customer_name TEXT,
            amount NUMERIC,
            loaded_at TIMESTAMP DEFAULT NOW()
        )
    """)

    cursor.execute("""
        INSERT INTO airflow_orders (order_id, customer_name, amount)
        VALUES (1, 'Ali Khan', 49.99)
        ON CONFLICT (order_id) DO UPDATE SET
            customer_name = EXCLUDED.customer_name,
            amount = EXCLUDED.amount,
            loaded_at = NOW()
    """)

    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM airflow_orders")
    count = cursor.fetchone()[0]
    print(f"airflow_orders now has {count} row(s)")

    conn.close()

with DAG(
    dag_id="real_postgres_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["learning", "postgres"],
) as dag:

    load_task = PythonOperator(
        task_id="extract_and_load",
        python_callable=extract_and_load,
    )
