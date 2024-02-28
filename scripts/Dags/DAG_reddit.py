import datetime
import pendulum

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def call_my_script():
    exec(open("/home/cissy/repos/RedditThread_ETL/scripts/Reddit_Scraping.py").read())


with DAG(
    dag_id="Reddit_pipeline_DAG",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2024, 2, 28, tz="EST"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(seconds=60),
    tags=["reddit_pipeline"],
) as dag:
        run_my_script = PythonOperator(
        task_id='run_my_python_script',
        python_callable=call_my_script,
    )