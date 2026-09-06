# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from datetime import datetime

# def extract():
#     print("Extracting data from source...")
#     return "raw_data"

# def transform():
#     print("Transforming data...")
#     return "transformed_data"

# def load():
#     print("Loading data into warehouse...")

# with DAG(
#     dag_id="my_first_pipeline",
#     start_date=datetime(2026, 1, 1),
#     schedule="@daily",
#     catchup=False,
#     tags=["learning"],
# ) as dag:

#     extract_task = PythonOperator(
#         task_id="extract",
#         python_callable=extract,
#     )

#     transform_task = PythonOperator(
#         task_id="transform",
#         python_callable=transform,
#     )

#     load_task = PythonOperator(
#         task_id="load",
#         python_callable=load,
#     )

#     extract_task >> transform_task >> load_task



from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract(**context):
    print("Extracting data from source...")
    data = "raw_order_data"
    context["ti"].xcom_push(key="extracted_data", value=data)

def transform(**context):
    data = context["ti"].xcom_pull(key="extracted_data", task_ids="extract")
    print(f"Transforming: {data}")
    transformed = data.upper()
    context["ti"].xcom_push(key="transformed_data", value=transformed)

def load(**context):
    data = context["ti"].xcom_pull(key="transformed_data", task_ids="transform")
    print(f"Loading into warehouse: {data}")

with DAG(
    dag_id="my_first_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["learning"],
) as dag:

    extract_task = PythonOperator(task_id="extract", python_callable=extract)
    transform_task = PythonOperator(task_id="transform", python_callable=transform)
    load_task = PythonOperator(task_id="load", python_callable=load)

    extract_task >> transform_task >> load_task


