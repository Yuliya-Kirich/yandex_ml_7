from io import BytesIO

import boto3
import pandas as pd


BUCKET = "mlops-module7-final-kirichenko"
PROCESSED_KEY = "processed/uber_processed.csv"
S3_ENDPOINT = "https://storage.yandexcloud.net"


def load_data():
    from io import BytesIO

    import boto3
    import pandas as pd

    bucket = "mlops-module7-final-kirichenko"
    processed_key = "processed/uber_processed.csv"
    s3_endpoint = "https://storage.yandexcloud.net"

    s3 = boto3.client("s3", endpoint_url=s3_endpoint)

    response = s3.get_object(
        Bucket=bucket,
        Key=processed_key,
    )

    df = pd.read_csv(BytesIO(response["Body"].read()))

    print(f"Загружено строк: {len(df)}")
    print(f"Количество столбцов: {len(df.columns)}")

    return df

def train_model(
    df,
    n_estimators: int = 100,
    learning_rate: float = 0.1,
):
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.model_selection import train_test_split

    features = [
        "pickup_latitude",
        "pickup_longitude",
        "dropoff_latitude",
        "dropoff_longitude",
        "passenger_count",
    ]

    X = df[features]
    y = df["fare_amount"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = GradientBoostingRegressor(
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        max_depth=3,
        random_state=42,
    )

    model.fit(X_train, y_train)

    print(
        f"Модель обучена: "
        f"n_estimators={n_estimators}, "
        f"learning_rate={learning_rate}"
    )

    return model, X_test, y_test

def evaluate(model, X_test, y_test):

    from sklearn.metrics import mean_squared_error

    predictions = model.predict(X_test)
    rmse = mean_squared_error(y_test, predictions) ** 0.5

    print(f"RMSE: {rmse:.4f}")
    return rmse

def save_model(model, model_name: str = "best_taxi_model"):
    from io import BytesIO

    import boto3
    import joblib

    buffer = BytesIO()
    joblib.dump(model, buffer)
    buffer.seek(0)

    key = f"models/{model_name}.joblib"

    s3 = boto3.client(
        "s3",
        endpoint_url="https://storage.yandexcloud.net",
    )

    s3.upload_fileobj(
        buffer,
        "mlops-module7-final-kirichenko",
        key,
    )

    model_path = f"s3://mlops-module7-final-kirichenko/{key}"
    print(f"Модель сохранена: {model_path}")

    return model_path

def evaluate_models(
    model_1,
    X_test_1,
    y_test_1,
    model_2,
    X_test_2,
    y_test_2,
):
    from sklearn.metrics import mean_squared_error

    predictions_1 = model_1.predict(X_test_1)
    rmse_1 = mean_squared_error(y_test_1, predictions_1) ** 0.5

    predictions_2 = model_2.predict(X_test_2)
    rmse_2 = mean_squared_error(y_test_2, predictions_2) ** 0.5

    print(f"Модель 1 — RMSE: {rmse_1:.4f}")
    print(f"Модель 2 — RMSE: {rmse_2:.4f}")

    if rmse_1 <= rmse_2:
        print("Лучшая модель: train_model_1")
        return model_1, "train_model_1", rmse_1

    print("Лучшая модель: train_model_2")
    return model_2, "train_model_2", rmse_2
