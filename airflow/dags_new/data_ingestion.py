import datetime
import os
import logging

from ingest_script import ingest_data
from convert import parquet2csv_task

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
URL_PREFIX = 'https://d37ci6vzurychx.cloudfront.net/trip-data' 
URL_TEMPLATE = URL_PREFIX + '/yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.parquet' # will make this execution date (thanks to airflow)
OUTPUT_FILE_TEMPLATE = AIRFLOW_HOME + '/output_{{ execution_date.strftime(\'%Y-%m\') }}.parquet'
OUTPUT_FILE_TEMPLATE_CSV = AIRFLOW_HOME + '/output_{{ execution_date.strftime(\'%Y-%m\') }}.csv'
TABLE_NAME_TEMPLATE = 'yellow_taxi_{{ execution_date.strftime(\'%Y_%m\') }}'
USER = os.environ.get("PG_USER")
PASSWORD = os.environ.get("PG_PASSWORD")
HOST = os.environ.get("PG_HOST")
PORT = os.environ.get("PG_PORT")
DATABASE = os.environ.get("PG_DATABASE")

local_workflow = DAG(
    dag_id="data_ingestion_dag",
    schedule_interval="0 6 2 * *",
    start_date = datetime(2021,1,1)
)

with local_workflow:
    # So it doesn't run many times it just runs once for every scheduled date
    download_task = BashOperator(
        task_id = "download_task",
        # use jinja for {{}}, this run whats is specified in "0 6 2 * *" and datetime(2021,1,1) or if we delect rerun in web.
        bash_command = f'curl -sSL {URL_TEMPLATE} > {OUTPUT_FILE_TEMPLATE}'
        #'echo "{{ ds }}" "{{ execution_date.strftime(\'%Y-%m\') }}"'
    )

    parquet2csv_task = PythonOperator(
        task_id = "parquet2csv_task",
        python_callable=parquet2csv_task,
        op_kwargs={
            "parquet_file": OUTPUT_FILE_TEMPLATE,
            "csv_file": OUTPUT_FILE_TEMPLATE_CSV
        },
    )


    ingest_task = PythonOperator(
        task_id = "ingest_task",
        python_callable=ingest_data,
        # user = root
        # password = root
        # host = data-engineering-zoomcamp-pgdatabase-1
        # port = 5432
        # db = ny_taxi
        op_kwargs={
            "user": USER,
            "password": PASSWORD,
            "host": HOST,
            "port": PORT,
            "db": DATABASE,
            "table_name": TABLE_NAME_TEMPLATE,
            "csv_file": OUTPUT_FILE_TEMPLATE_CSV,
            #"execution_date":
        },
    )
    download_task >> parquet2csv_task >> ingest_task