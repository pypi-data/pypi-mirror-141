from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

default_args = {"owner": ownertoreplace, "start_date": datetime.now()}

dag = DAG(
    dag_id,
    schedule_interval=scheduletoreplace,
    default_args=default_args,
    catchup=False,
)

with dag:
    t1 = DockerOperator(
        task_id="docker_command",
        image=imagetoreplace,
        api_version="auto",
        auto_remove=True,
        command=commandtoreplace,
    )
