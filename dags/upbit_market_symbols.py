# dags/upbit_market_symbols.py

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="upbit_market_symbols",
    start_date=datetime(2023, 1, 1),
    schedule_interval="*/15 * * * *",
    default_args=default_args,
    catchup=False,
    tags=["upbit", "symbols"],
) as dag:

    run_collector = BashOperator(
        task_id="collect_symbols",
        bash_command="python3 /opt/airflow/external/collect_upbit_symbols.py"
    )
