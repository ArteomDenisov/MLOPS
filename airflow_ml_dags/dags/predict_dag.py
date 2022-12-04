from datetime import timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.models import Variable
from airflow.utils import timezone
from docker.types import Mount


default_args = {
    "owner": "airflow",
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

MODEL_PATH = Variable.get("MODEL_PATH")


def days_ago(n: int):
    today = timezone.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    return today - timedelta(days=n)


with DAG(
        "prediction",
        default_args=default_args,
        schedule_interval="@daily",
        start_date=days_ago(5),
) as dag:

    predict = DockerOperator(
        image="airflow-predict",
        command="--data-path /data/processed/{{ ds }} --prediction-path /data/predictions/{{ ds }} --model-path " + MODEL_PATH,
        network_mode="bridge",
        task_id="predict",
        do_xcom_push=False,
        mount_tmp_dir=False,
        # !!! HOST folder(NOT IN CONTAINER) replace with yours !!!
        mounts=[Mount(source="/Users/user/PycharmProjects/homework02/ArtemDenisov/airflow_ml_dags/data/",
                      target="/data",
                      type='bind'),
                Mount(source="/Users/user/PycharmProjects/homework02/ArtemDenisov/airflow_ml_dags/models/",
                      target="/models",
                      type='bind'),
                ]
    )

    predict
