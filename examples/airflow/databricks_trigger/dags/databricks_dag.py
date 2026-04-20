from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    "email_on_failure": False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'trigger_databricks_job',
    default_args=default_args,
    description='Simple DAG to trigger DB job',
    schedule_interval=None,
    start_date=datetime(2026,4,20),
    catchup=False,
) as dag:

    # Replace JOB_ID with your actual databricks job id
    run_now = DatabricksRunNowOperator(
        task_id='run_my_job',
        databricks_conn_id='databricks_default',
        job_id=1065615312316575,
    )

    run_now
