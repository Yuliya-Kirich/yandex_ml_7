from datetime import datetime
from io import StringIO

import pandas as pd
from airflow.sdk import dag, task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from taxi_schema import taxi_schema


BUCKET = "mlops-module7-final-kirichenko"
RAW_KEY = "raw/uber.csv"
PROCESSED_KEY = "processed/uber_processed.csv"
AWS_CONN_ID = "yandex_s3"


@dag(
    dag_id="final_task_dag",
    schedule="@hourly",
    start_date=datetime(2026, 11, 1),
    catchup=False,
    tags=["mlops", "taxi", "s3"],
)
def taxi_data_pipeline():

    @task
    def process_uber_data():
        hook = S3Hook(aws_conn_id=AWS_CONN_ID)

        csv_content = hook.read_key(
            key=RAW_KEY,
            bucket_name=BUCKET,
        )
        df = pd.read_csv(StringIO(csv_content))

        print(f"Загружено строк: {len(df)}")

        df = df.loc[:, ~df.columns.str.startswith("Unnamed")]

        df["pickup_datetime"] = pd.to_datetime(
            df["pickup_datetime"],
            errors="coerce",
            utc=True,
        ).dt.tz_localize(None)

        df = df.dropna()

        df = df[
            (df["fare_amount"] > 0)
            & (df["passenger_count"].between(1, 6))
            & (df["pickup_longitude"].between(-180, 180))
            & (df["dropoff_longitude"].between(-180, 180))
            & (df["pickup_latitude"].between(-90, 90))
            & (df["dropoff_latitude"].between(-90, 90))
        ].copy()

        validated_df = taxi_schema.validate(df)

        print(f"После проверки осталось строк: {len(validated_df)}")

        output = validated_df.to_csv(index=False)

        hook.load_string(
            string_data=output,
            key=PROCESSED_KEY,
            bucket_name=BUCKET,
            replace=True,
        )

        print(f"Сохранено: s3://{BUCKET}/{PROCESSED_KEY}")

    process_uber_data()


taxi_data_pipeline()