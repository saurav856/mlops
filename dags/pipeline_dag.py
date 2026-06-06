from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "saurav",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="mlops_pipeline",
    default_args=default_args,
    description="Automated MLOps pipeline for credit card default prediction",
    schedule_interval="@weekly",
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

    ingest = BashOperator(
        task_id="data_ingestion",
        bash_command="cd /opt/airflow && conda run -n mlops_env python3 scripts/ingest.py",
    )

    preprocess = BashOperator(
        task_id="data_preprocessing",
        bash_command="cd /opt/airflow && conda run -n mlops_env python3 scripts/preprocess.py",
    )

    train = BashOperator(
        task_id="model_training",
        bash_command="cd /opt/airflow && conda run -n mlops_env python3 scripts/train.py",
    )

    monitor = BashOperator(
        task_id="model_monitoring",
        bash_command="cd /opt/airflow && conda run -n mlops_env python3 scripts/monitor.py",
    )

    ingest >> preprocess >> train >> monitor