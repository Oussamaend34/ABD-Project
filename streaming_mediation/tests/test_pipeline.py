"""Unit tests for the normalize function in the transformer module."""

from datetime import datetime

import pytest

from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    TimestampType,
    IntegerType,
    DoubleType,
)
from src.pipeline import normalize, tag_cdrs


@pytest.fixture(scope="module")
def _spark():
    """Create a Spark session for testing."""
    return (
        SparkSession.builder.master("local[*]").appName("NormalizeTest").getOrCreate()
    )


def test_normalize_with_realistic_fields(_spark):
    """
    Test the normalize function with realistic fields for voice, SMS, and data CDRs.
    """
    # Voice CDR
    voice_data = [
        (
            "v1",
            "voice",
            datetime(2025, 5, 1, 12, 0, 0),
            "0612345678",
            "0698765432",
            120,
            "city_1",
            "4G",
        ),
        (
            "v2",
            "voice",
            datetime(2025, 5, 1, 12, 0, 0),
            "212612345678",
            "9999698765432",
            300,
            "INVALID!!!@#",
            "4G",
        ),
        (
            None,
            "voice",
            None,
            "212612345678",
            "212698765432",
            -300,
            "rabat_center_3",
            "4G",
        ),
        (
            "v4",
            "voice",
            datetime(2025, 5, 1, 12, 0, 0),
            "212612345678",
            None,
            None,
            "rabat_center_3",
            "4G",
        ),
    ]
    voice_schema = StructType(
        [
            StructField("uuid", StringType()),
            StructField("record_type", StringType()),
            StructField("timestamp", TimestampType()),
            StructField("caller_id", StringType()),
            StructField("callee_id", StringType()),
            StructField("duration_sec", IntegerType()),
            StructField("cell_id", StringType()),
            StructField("technology", StringType()),
        ]
    )
    voice_df = _spark.createDataFrame(voice_data, schema=voice_schema)

    # SMS CDR
    sms_data = [
        (
            "s1",
            "sms",
            datetime(2025, 5, 1, 12, 5, 0),
            "212612300000",
            "212698800000",
            "cell-02",
            "3G",
        )
    ]
    sms_schema = StructType(
        [
            StructField("uuid", StringType()),
            StructField("record_type", StringType()),
            StructField("timestamp", TimestampType()),
            StructField("sender_id", StringType()),
            StructField("receiver_id", StringType()),
            StructField("cell_id", StringType()),
            StructField("technology", StringType()),
        ]
    )
    sms_df = _spark.createDataFrame(sms_data, schema=sms_schema)

    # Data EDR
    data_data = [
        (
            "d1",
            "data",
            datetime(2025, 5, 1, 12, 10, 0),
            "212655555555",
            360,
            100.5,
            "cell-03",
            "5G",
        )
    ]
    data_schema = StructType(
        [
            StructField("uuid", StringType()),
            StructField("record_type", StringType()),
            StructField("timestamp", TimestampType()),
            StructField("user_id", StringType()),
            StructField("duration_sec", IntegerType()),
            StructField("data_volume_mb", DoubleType()),
            StructField("cell_id", StringType()),
            StructField("technology", StringType()),
        ]
    )
    data_df = _spark.createDataFrame(data_data, schema=data_schema)

    # Union all records to simulate mixed Kafka stream
    combined_df = voice_df.unionByName(sms_df, allowMissingColumns=True).unionByName(
        data_df, allowMissingColumns=True
    )

    normalized_df = normalize(combined_df)

    schema = StructType(
        [
            StructField("uuid", StringType(), True),
            StructField("record_type", StringType(), True),
            StructField("timestamp", TimestampType(), True),
            StructField("msisdn", StringType(), True),
            StructField("counterparty_msisdn", StringType(), True),
            StructField("duration_sec", IntegerType(), True),
            StructField("data_volume_mb", DoubleType(), True),
            StructField("cell_id", StringType(), True),
            StructField("technology", StringType(), True),
            StructField("status", StringType(), True),
        ]
    )

    normalized_df = _spark.createDataFrame(normalized_df.rdd, schema)

    tagged_df = tag_cdrs(normalized_df)
    rows = tagged_df.collect()

    assert rows[0].msisdn == "212612345678"
    assert rows[0].counterparty_msisdn == "212698765432"
    assert rows[0].duration_sec == 120
    assert rows[0].data_volume_mb is None
    assert rows[0].status == "ok"

    assert rows[1].status == "partial"
