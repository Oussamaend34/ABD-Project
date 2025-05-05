"""
Streaming Mediation Pipeline with Spark Structured Streaming + Kafka + Avro + Schema Registry.
"""

from functools import lru_cache
import re

import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import from_avro, to_avro
from pyspark.sql.functions import udf
from pyspark.sql.types import (
    StringType,
    BinaryType,
    TimestampType,
    IntegerType,
    DoubleType,
)
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when, regexp_extract
from confluent_kafka.schema_registry import SchemaRegistryClient, RegisteredSchema


# ========== CONFIGURATION ==========
VOICE_TOPIC = "cdr.voice"
SMS_TOPIC = "cdr.sms"
DATA_TOPIC = "cdr.data"
VOICE_SUBJECT = f"{VOICE_TOPIC}-value"
SMS_SUBJECT = f"{SMS_TOPIC}-value"
DATA_SUBJECT = f"{DATA_TOPIC}-value"
TOPIC_OK_SINK = "cdr.ok"
SUBJECT_SINK = f"{TOPIC_OK_SINK}-value"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092,localhost:9093,localhost:9094"
SCHEMA_REGISTRY_URL = "http://localhost:8081"

# ========== SPARK SESSION ==========
spark = (
    SparkSession.builder.appName("streaming_mediation_pipeline")
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5,"
        "org.apache.spark:spark-avro_2.12:3.5.5",
    )
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

# ========== UDFs ==========
binary_to_string_udf = F.udf(lambda x: str(int.from_bytes(x, "big")), StringType())
int_to_binary_udf = F.udf(
    lambda value, byte_size: (value).to_bytes(byte_size, byteorder="big"), BinaryType()
)


def __normalize_msisdn(msisdn: str) -> str:
    """
    Normalize Moroccan MSISDN:
    - Remove spaces, dashes, parentheses, etc.
    - Convert local format (06/07) to international (2126/2127)
    """
    if msisdn is None:
        return None
    digits = re.sub(r"\D", "", msisdn)

    if digits.startswith("06") or digits.startswith("07"):
        digits = "212" + digits[1:]
    elif digits.startswith("00212"):
        digits = digits[2:]
    elif digits.startswith("212"):
        pass
    elif digits.startswith("+212"):
        digits = digits[1:]

    return digits if digits.startswith("212") else None


normalize_msisdn_udf = udf(__normalize_msisdn, StringType())


def normalize(df: DataFrame) -> DataFrame:
    """
    Normalize raw CDR/EDR DataFrame to the unified normalized schema.
    """

    optional_fields = ["sender_id", "receiver_id", "user_id", "data_volume_mb"]
    for field in optional_fields:
        if field not in df.columns:
            df = df.withColumn(field, F.lit(None))
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
            .when(col("record_type") == "data", col("duration_sec"))
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


def tag_cdrs(df: DataFrame) -> DataFrame:
    """
    Tags CDRs with 'status':
    - 'error': if msisdn is missing/invalid or both uuid and timestamp missing
    - 'invalid_usage': if usage fields are corrupt
    - 'partial': if metadata (cell_id, technology) is missing or malformed
    """
    msisdn_valid_regex = r"^212[6-7][0-9]{8}$"
    cellid_pattern = r"^[a-z][a-z_]*?_[0-9]*$"

    return df.withColumn(
        "status",
        when(
            col("msisdn").isNull()
            | (regexp_extract(col("msisdn"), msisdn_valid_regex, 0) == "")
            | (col("uuid").isNull() & col("timestamp").isNull()),
            "error",
        )
        .when(
            (col("record_type") == "voice")
            & (
                col("duration_sec").isNull()
                | (col("duration_sec") < 0)
                | (col("duration_sec") > 7200)
            ),
            "invalid_usage",
        )
        .when(
            (col("record_type") == "data")
            & (
                col("data_volume_mb").isNull()
                | (col("duration_sec") < 0)
                | (col("duration_sec") > 86400)
                | (col("data_volume_mb") < 0)
                | (col("data_volume_mb") > 100000)
            ),
            "invalid_usage",
        )
        .when(
            col("cell_id").isNull()
            | (regexp_extract(col("cell_id"), cellid_pattern, 0) == "")
            | col("technology").isNull()
            | col("timestamp").isNull()
            | col("uuid").isNull(),
            "partial",
        )
        .otherwise("ok"),
    )


def deduplicate_streaming(df: DataFrame, watermark_delay="30 minutes") -> DataFrame:
    """
    Deduplicate streaming CDRs in real time:
    - Keeps first UUID seen within the watermark window.
    - Drops late or duplicate UUIDs.
    - Requires 'uuid' and 'timestamp' fields.
    """
    return df.withWatermark("timestamp", watermark_delay).dropDuplicates(["uuid"])


# ========== SCHEMA RESOLVER ==========
@lru_cache()
def get_latest_schema_str(subject: str) -> RegisteredSchema:
    """
    Get the latest schema string from the schema registry.
    """
    sr = SchemaRegistryClient({"url": SCHEMA_REGISTRY_URL})
    return sr.get_latest_version(subject)


voice_schema_str = get_latest_schema_str(VOICE_SUBJECT).schema.schema_str
sms_schema_str = get_latest_schema_str(SMS_SUBJECT).schema.schema_str
data_schema_str = get_latest_schema_str(DATA_SUBJECT).schema.schema_str

# ========== STREAM FROM KAFKA ==========
voice_kafka_df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)
    .option("subscribe", VOICE_TOPIC)
    .option("startingOffsets", "latest")
    .load()
)
sms_kafka_df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)
    .option("subscribe", SMS_TOPIC)
    .option("startingOffsets", "latest")
    .load()
)
data_kafka_df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)
    .option("subscribe", DATA_TOPIC)
    .option("startingOffsets", "latest")
    .load()
)

# ========== DECODE CONFLUENT WIRE FORMAT ==========
# Drop magic byte (1 byte) + schema ID (4 bytes) => first 5 bytes
voice_kafka_df = voice_kafka_df.withColumn(
    "payload", F.expr("substring(value, 6, length(value) - 5)")
).withColumn("schemaId", binary_to_string_udf(F.expr("substring(value, 2, 4)")))
sms_kafka_df = sms_kafka_df.withColumn(
    "payload", F.expr("substring(value, 6, length(value) - 5)")
).withColumn("schemaId", binary_to_string_udf(F.expr("substring(value, 2, 4)")))
data_kafka_df = data_kafka_df.withColumn(
    "payload", F.expr("substring(value, 6, length(value) - 5)")
).withColumn("schemaId", binary_to_string_udf(F.expr("substring(value, 2, 4)")))
# ========== DESERIALIZE AVRO PAYLOAD ==========

voice_decoded_df = voice_kafka_df.select(
    from_avro(F.col("payload"), voice_schema_str).alias("record")
)
sms_decoded_df = sms_kafka_df.select(
    from_avro(F.col("payload"), sms_schema_str).alias("record")
)
data_decoded_df = data_kafka_df.select(
    from_avro(F.col("payload"), data_schema_str).alias("record")
)
# ========== UNION ALL DECODED DATAFRAMES ==========
union_df = voice_decoded_df.unionByName(
    sms_decoded_df, allowMissingColumns=True
).unionByName(data_decoded_df, allowMissingColumns=True)
# Flatten struct fields from "record"
result_df = union_df.select("record.*")

result_df = result_df.withColumn("uuid", F.expr("uuid()")).withColumn(
    "timestamp", F.to_timestamp(F.col("timestamp"), "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'")
)
# ========== NORMALIZE ==========
result_df = normalize(result_df)

result_df = result_df.select(
    col("uuid").cast(StringType()),
    col("record_type").cast(StringType()),
    col("timestamp").cast(TimestampType()),
    col("msisdn").cast(StringType()),
    col("counterparty_msisdn").cast(StringType()),
    col("duration_sec").cast(IntegerType()),
    col("data_volume_mb").cast(DoubleType()),
    col("cell_id").cast(StringType()),
    col("technology").cast(StringType()),
    col("status").cast(StringType()),
)

result_df = tag_cdrs(result_df)


required_ok_fields = ["msisdn", "cell_id", "technology", "record_type", "timestamp"]
result_df = result_df.filter(F.col("status") == "ok")
result_df = result_df.filter(
    (F.col("status") == "ok")
    & F.col("msisdn").isNotNull()
    & F.col("cell_id").isNotNull()
    & F.col("technology").isNotNull()
    & F.col("record_type").isNotNull()
    & F.col("timestamp").isNotNull()
)
# Optional: verify all required fields are non-null
for field in required_ok_fields:
    result_df = result_df.filter(F.col(field).isNotNull())
# ========== OUTPUT ==========
latest_version_analyzed_data = get_latest_schema_str(SUBJECT_SINK)

result_df = result_df.select(
    to_avro(F.struct("*"), latest_version_analyzed_data.schema.schema_str).alias(
        "value"
    ),
)
magicByteBinary = int_to_binary_udf(F.lit(0), F.lit(1))
schemaIdBinary = int_to_binary_udf(
    F.lit(latest_version_analyzed_data.schema_id), F.lit(4)
)
result_df = result_df.withColumn(
    "value", F.concat(magicByteBinary, schemaIdBinary, col("value"))
)

print("Writing to Kafka topic:", TOPIC_OK_SINK)
query = (
    result_df.writeStream.format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)
    .option("topic", TOPIC_OK_SINK)
    .outputMode("append")
    .option("checkpointLocation", "checkpoint")
    .start()
)
query.awaitTermination()
