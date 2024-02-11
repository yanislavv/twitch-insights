from airflow import DAG
from airflow.operators.mysql_operator import MySqlOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'Yanislav',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,

}


dag = DAG(
    'mysql_query_dag',
    default_args=default_args,
    description='SQl queries to monitor the ingestion of the messages.',
    schedule_interval='@daily',
    tags=['monitoring'],
    catchup=False
)


query_1 = "INSERT INTO `new_table` (`idnew_table`) VALUES (1);"


task_execute_query_1 = MySqlOperator(
    task_id='execute_query_1',
    mysql_conn_id='local-mysql',  # Specify the MySQL connection ID
    sql=query_1,
    dag=dag,
)

task_execute_query_1
