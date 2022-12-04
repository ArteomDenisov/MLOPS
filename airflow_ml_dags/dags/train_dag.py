from datetime import timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils import timezone
from airflow.models import Variable
from docker.types import Mount


def days_ago(n: int):
    today = timezone.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    return today - timedelta(days=n)


MODEL_PATH = Variable.get("MODEL_PATH")
# !!! HOST folder(NOT IN CONTAINER) replace with yours !!!
MOUNT_DATA = Mount(source="/home/artem/artem_denisov/airflow_ml_dags/data/",
                   target="/data",
                   type='bind')
MOUNT_MODEL = Mount(source="/home/artem/artem_denisov/airflow_ml_dags/models/",
                    target="/models",
                    type='bind')


default_args = {
    "owner": "airflow",
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
        "training",
        default_args=default_args,
        schedule_interval="@weekly",
        start_date=days_ago(5),
) as dag:
    download = DockerOperator(
        image="airflow-download",
        command="--raw /data/raw/{{ ds }} --processed /data/processed/{{ ds }}",
        network_mode="bridge",
        task_id="download",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[MOUNT_DATA, MOUNT_MODEL]
    )

    split = DockerOperator(
        image="airflow-split",
        command="--processed /data/processed/{{ ds }}",
        network_mode="bridge",
        task_id="split",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[MOUNT_DATA]
    )

    transform = DockerOperator(
        image="airflow-transform",
        command="--data-path /data/processed/{{ ds }} --model-path " + MODEL_PATH,
        network_mode="bridge",
        task_id="transform",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[MOUNT_DATA]
    )

    train = DockerOperator(
        image="airflow-train",
        command="--data-path /data/processed/{{ ds }} --model-path " + MODEL_PATH,
        network_mode="bridge",
        task_id="train",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[MOUNT_DATA, MOUNT_MODEL]
    )

    validate = DockerOperator(
        image="airflow-validate",
        command="--data-path /data/processed/{{ ds }} --model-path " + MODEL_PATH,
        network_mode="bridge",
        task_id="validate",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[MOUNT_DATA, MOUNT_MODEL]
    )

    download >> split >> transform >> train >> validate
