"""
Unit tests for the tag_cdrs function in the pipeline module.
"""

from datetime import datetime

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
    TimestampType,
)

from src.pipeline import tag_cdrs


@pytest.fixture(scope="module")
def _spark():
    """Create a Spark session for testing."""
    return (
        SparkSession.builder.master("local[*]").appName("CDRTaggingTest").getOrCreate()
    )


def test_tag_cdrs(_spark):
    """
    Test the tag_cdrs function with various CDR records.
    This test includes cases for valid, partial, error, and invalid_usage records.
    """
    schema = StructType(
        [
            StructField("uuid", StringType(), True),
            StructField("record_type", StringType(), True),
            StructField("timestamp", TimestampType(), True),
            StructField("msisdn", StringType(), True),
            StructField("callee_id", StringType(), True),
            StructField("duration_sec", IntegerType(), True),
            StructField("session_duration_sec", IntegerType(), True),
            StructField("data_volume_mb", DoubleType(), True),
            StructField("cell_id", StringType(), True),
            StructField("technology", StringType(), True),
        ]
    )

    data = [
        # ok
        (
            "v1",
            "voice",
            datetime(2025, 5, 1, 12, 0),
            "212612345678",
            "212698765432",
            300,
            None,
            None,
            "rabat_center_3",
            "4G",
        ),
        # partial (bad cell_id format)
        (
            "v2",
            "voice",
            datetime(2025, 5, 1, 12, 0),
            "212612345679",
            "212698765433",
            200,
            None,
            None,
            "invalidCell",
            "4G",
        ),
        # error (invalid msisdn)
        (
            "v3",
            "voice",
            datetime(2025, 5, 1, 12, 0),
            "999",
            "212698765434",
            100,
            None,
            None,
            "rabat_center_2",
            "4G",
        ),
        # invalid_usage (data volume too high)
        (
            "d1",
            "data",
            datetime(2025, 5, 1, 13, 0),
            "212623456789",
            None,
            None,
            3600,
            200000.0,
            "casa_south_5",
            "5G",
        ),
    ]

    df = _spark.createDataFrame(data, schema=schema)
    tagged_df = tag_cdrs(df)
    result = {row.uuid: row.status for row in tagged_df.collect()}

    assert result["v1"] == "ok"
    assert result["v2"] == "partial"
    assert result["v3"] == "error"
    assert result["d1"] == "invalid_usage"
