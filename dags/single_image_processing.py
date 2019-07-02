# encoding: utf-8

import os

from airflow import DAG
from airflow.operators.python_operator import PythonOperator


from workflow.tasks import download_file, image_to_md5, image_to_gray, on_workflow_error,\
    on_workflow_success, save_image_metadata


DATA_PATH = '/usr/local/airflow/data'


def generate_image_processing_subtask(parent_dag_name, start_date, schedule_interval, url, index):
    """
    :param parent_dag_name:
    :param start_date:
    :param schedule_interval:
    :param url:
    :param index:
    :param work_dir:
    :return:
    """
    child_dag_name = "image_etl_%d" % index
    work_dir = os.path.join(DATA_PATH, "wflow_%d_improc" % index)

    dag = DAG(
        '%s.%s' % (parent_dag_name, child_dag_name),
        schedule_interval=schedule_interval,
        start_date=start_date,
    )

    extract = PythonOperator(
        task_id='extract_task_%d' % index,
        python_callable=download_file,
        op_kwargs={'url': url, 'work_dir_path': work_dir},
        dag=dag,
    )

    md5 = PythonOperator(
        task_id='md5_task_%d' % index,
        provide_context=True,
        python_callable=image_to_md5,
        op_kwargs={'ref_number': index},
        dag=dag,
    )

    gray = PythonOperator(
        task_id='gray_task_%d' % index,
        provide_context=True,
        python_callable=image_to_gray,
        op_kwargs={'ref_number': index},
        dag=dag,
    )

    save_metadata = PythonOperator(
        task_id='save_metadata_task_%d' % index,
        provide_context=True,
        python_callable=save_image_metadata,
        op_kwargs={'ref_number': index},
        dag=dag,
    )

    etl_success = PythonOperator(
        task_id='success_task_%d' % index,
        python_callable=on_workflow_success,
        op_kwargs={'url': url, 'working_dir_path': work_dir},
        trigger_rule='none_failed',
        dag=dag,
    )

    etl_error = PythonOperator(
        task_id='error_task_%d' % index,
        python_callable=on_workflow_error,
        op_kwargs={'url': url, 'working_dir_path': work_dir},
        trigger_rule='one_failed',
        dag=dag,
    )
    # define subtask workflow

    extract >> [md5, gray] >> save_metadata >> [etl_error, etl_success]

    return dag
