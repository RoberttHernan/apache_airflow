from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id="dag_test_201700870",
    description="Test DAG for student ID 201700870",
    start_date=datetime(2024, 1, 1),
    schedule=timedelta(days=1),
    catchup=False,
    tags=["test", "201700870"],
) as dag:
    start = EmptyOperator(task_id="start_201700870")
    end = EmptyOperator(task_id="end_201700870")

    start >> end

#agrega commentario para que el DAG sea más descriptivo
