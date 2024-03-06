import datetime
import pendulum
import sys
sys.path.append("/home/cissy/repos/RedditThread_ETL/scripts")
from Reddit_Scraping import run_update

from airflow import DAG
from airflow.operators.python_operator import PythonOperator


with DAG(
    dag_id="Reddit_pipeline_DAG",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2024, 2, 28, tz="EST"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=5),
    tags=["reddit_pipeline"],
) as dag:
        run_my_script = PythonOperator(
        task_id='Load_reddit_posts_to_mongoDB',
        python_callable=run_update,
    )

run_my_script