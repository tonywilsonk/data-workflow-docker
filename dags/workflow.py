# encoding: utf-8

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator


import single_image_processing


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 6, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

DATA_PATH = '/usr/local/airflow/data'

PARENT_DAG_NAME = 'images_processing_dag'

# helpers functions for dynamic workflow definition


def get_urls():
    # read the file and run the workflow
    urls = []

    with open('/usr/local/airflow/dags/urls.txt') as f:
        for line in f:
            urls.append(line.rstrip('\n'))

    return urls


def get_sub_dag(url, index, dag):

    sub_dag = SubDagOperator(
        subdag=single_image_processing.generate_image_processing_subtask(PARENT_DAG_NAME, dag.start_date,
                                                                         dag.schedule_interval, url, index),
        task_id="image_etl_%d" % index,
        dag=dag,
    )

    return sub_dag


main_dag = DAG(
    dag_id=PARENT_DAG_NAME,
    schedule_interval=None,
    start_date=datetime(2019, 6, 1),
    default_args=default_args
)


start = DummyOperator(
        task_id='start_task',
        dag=main_dag,
    )

end = DummyOperator(
        task_id='end_task',
        trigger_rule='all_done',
        dag=main_dag,
    )

tsk = []


for i, u in enumerate(get_urls()):
    tsk.append(get_sub_dag(url=u, index=i, dag=main_dag))


start >> tsk >> end


