from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id='sensor_factory_pipeline', # The unique name Airflow uses to find this in the UI
    start_date=datetime(2026, 3, 28), # The 'Birthday' of the DAG; it won't run before this
    schedule_interval=None,           # 'None' means this only runs when you click 'Play' in the UI
    catchup=False,                    # Prevents Airflow from trying to run 'missed' days from the past
    tags=['production', 'sensors']    # Labels to help you filter your 1,000s of DAGs in the UI
) as dag:

# =============================================================================
    # 3. THE OPERATORS
    # An Operator is a template for a single unit of work. 
    # Here we use BashOperator, which literally runs a command in the terminal.
    # =============================================================================

    # TASK 1
    # This triggers your 15-million-row generator script.
    t1 = BashOperator(
        task_id='generate_raw_data',
        bash_command='python3 /opt/airflow/scripts/generator.py'
    )

# TASK 2
    # We use 'spark-submit' because it allows Spark to manage memory and 
    # parallelize the cleaning of those 15M rows.
    t2 = BashOperator(
        task_id='spark_clean_data',
        bash_command='spark-submit --master local[*] /opt/airflow/scripts/clean_data.py'
    )

# TASK 3
    # This takes the clean data and calculates averages, max, and min.
    t3 = BashOperator(
        task_id='spark_analyze_data',
        bash_command='python3 /opt/airflow/scripts/analyze_data.py'
    )

# TASK 4
    # Streamlit is 'watching' its app.py file. By 'touching' it, we update 
    # its timestamp, which tricks Streamlit into refreshing the dashboard.
    t4 = BashOperator(
        task_id='refresh_streamlit',
        bash_command='touch /opt/airflow/scripts/app.py'
    )

# =============================================================================
    # 4. THE FLOW (The "Dependencies")
    # The bitwise operators (>>) set the order of operations.
    # Airflow will not start t2 until t1 finishes with a 'Success' status.
    # =============================================================================
    t1 >> t2 >> t3 >> t4