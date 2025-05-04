"""
Pipeline for processing CDR/EDR data.
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when
from pyspark.sql import functions as F
from src.utils.helpers import normalize_msisdn_udf


def normalize(df: DataFrame) -> DataFrame:
    """
    Normalize raw CDR/EDR DataFrame to the unified normalized schema.
    """

    return (
        df.withColumn(
            "msisdn",
            when(col("record_type") == "voice", col("caller_id"))
            .when(col("record_type") == "sms", col("sender_id"))
            .when(col("record_type") == "data", col("user_id"))
            .otherwise(None),
        )
        .withColumn("msisdn", normalize_msisdn_udf(col("msisdn")))
        .withColumn(
            "counterparty_msisdn",
            when(col("record_type") == "voice", col("callee_id"))
            .when(col("record_type") == "sms", col("receiver_id"))
            .otherwise(F.lit(None)),
        )
        .withColumn(
            "counterparty_msisdn", normalize_msisdn_udf(col("counterparty_msisdn"))
        )
        .withColumn(
            "duration_sec",
            when(col("record_type") == "voice", col("duration_sec"))
            .when(col("record_type") == "data", col("session_duration_sec"))
            .otherwise(F.lit(None)),
        )
        .withColumn(
            "data_volume_mb",
            when(col("record_type") == "data", col("data_volume_mb")).otherwise(
                F.lit(None)
            ),
        )
        .withColumn("status", F.lit("ok"))
        .select(
            "uuid",
            "record_type",
            "timestamp",
            "msisdn",
            "counterparty_msisdn",
            "duration_sec",
            "data_volume_mb",
            "cell_id",
            "technology",
            "status",
        )
    )


def tag_identity_errors(df: DataFrame) -> DataFrame:
    """
    Tags CDRs with 'status' based on identity-critical fields.
    Must have:
    - a valid MSISDN
    - at least one of (uuid, timestamp)
    """

    df = df.withColumn(
        "status",
        when(col("msisdn").isNull(), "error")
        .when(col("uuid").isNull() & col("timestamp").isNull(), "error")
        .otherwise(col("status")),  # retain if already tagged (e.g., "ok" or "partial")
    )
    return df


def tag_usage_anomalies(df: DataFrame) -> DataFrame:
    """
    Tag CDRs with status = 'invalid_usage' if usage values are corrupt or unreasonable.
    Rules depend on record_type:
        - voice: duration must be 0 ≤ x ≤ 7200 sec
        - data: session and volume must be in sane ranges
    """
    df = df.withColumn(
        "status",
        when(
            (col("record_type") == "voice")
            & ((col("duration_sec") < 0) | (col("duration_sec") > 7200)),
            "invalid_usage",
        )
        .when(
            (col("record_type") == "data")
            & (
                (col("session_duration_sec") < 0)
                | (col("session_duration_sec") > 86400)
                | (col("data_volume_mb") < 0)
                | (col("data_volume_mb") > 100000)
            ),
            "invalid_usage",
        )
        .otherwise(col("status")),
    )
    return df
