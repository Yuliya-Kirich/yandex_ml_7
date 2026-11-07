import pandera.pandas as pa
from pandera import Column, Check


taxi_schema = pa.DataFrameSchema(
    {
        "key": Column(pa.String, nullable=False, unique=True),
        "pickup_datetime": Column(pa.DateTime, nullable=False),
        "pickup_longitude": Column(
            pa.Float64, checks=Check.in_range(-180, 180), nullable=True
        ),
        "pickup_latitude": Column(
            pa.Float64, checks=Check.in_range(-90, 90), nullable=True
        ),
        "dropoff_longitude": Column(
            pa.Float64, checks=Check.in_range(-180, 180), nullable=True
        ),
        "dropoff_latitude": Column(
            pa.Float64, checks=Check.in_range(-90, 90), nullable=True
        ),
        "passenger_count": Column(
            pa.Int64, checks=[Check.ge(1), Check.le(6)], nullable=True
        ),
        "fare_amount": Column(
            pa.Float64, checks=Check.ge(0), nullable=True
        ),
    },
    coerce=True,
)