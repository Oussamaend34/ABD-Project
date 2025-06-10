"""
This script creates all the necessary Kafka topics for the synthetic CDR generator.
It includes topics for voice, SMS, data, OK, and error CDRs.
"""

from typing import Sequence
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.admin import ClusterMetadata, TopicMetadata, PartitionMetadata
from confluent_kafka.schema_registry import SchemaRegistryClient, Schema


admin_config = {
    "bootstrap.servers": "localhost:9092,localhost:9093,localhost:9094",
}

sr_config = {
    "url": "http://localhost:8081",
}


admin_client = AdminClient(admin_config)
sr_client = SchemaRegistryClient(sr_config)

voice_cdr_topic = NewTopic("cdr.voice", num_partitions=3, replication_factor=1)  # type: ignore
sms_cdr_topic = NewTopic("cdr.sms", num_partitions=3, replication_factor=1)  # type: ignore
data_edr_topic = NewTopic("cdr.data", num_partitions=3, replication_factor=1)  # type: ignore
ok_cdr_topic = NewTopic("cdr.ok", num_partitions=3, replication_factor=1)  # type: ignore
error_cdr_topic = NewTopic("cdr.error", num_partitions=3, replication_factor=1)  # type: ignore
unratable_cdr_topic = NewTopic("cdr.unratable", num_partitions=3, replication_factor=1)

topic_results = admin_client.create_topics(
    [
        voice_cdr_topic,
        sms_cdr_topic,
        data_edr_topic,
        ok_cdr_topic,
        error_cdr_topic,
        unratable_cdr_topic,
    ]
)

with open("avro/voice_cdr.avsc", "r", encoding="utf-8") as f:
    voice_cdr_schema = f.read()

with open("avro/sms_cdr.avsc", "r", encoding="utf-8") as f:
    sms_cdr_schema = f.read()

with open("avro/data_edr.avsc", "r", encoding="utf-8") as f:
    data_edr_schema = f.read()

with open("avro/normalized_cdr.avsc", "r", encoding="utf-8") as f:
    ok_cdr_schema = f.read()

with open("avro/normalized_cdr_error.avsc", "r", encoding="utf-8") as f:
    error_cdr_schema = f.read()

with open("avro/unratable_cdr.avsc", "r", encoding="utf-8") as f:
    unratable_cdr_schema = f.read()

cdr_voice_schema = Schema(voice_cdr_schema, "AVRO")
cdr_sms_schema = Schema(sms_cdr_schema, "AVRO")
cdr_data_schema = Schema(data_edr_schema, "AVRO")
cdr_ok_schema = Schema(ok_cdr_schema, "AVRO")
cdr_error_schema = Schema(error_cdr_schema, "AVRO")
cdr_unratable_schema = Schema(unratable_cdr_schema, "AVRO")

print("Registering schemas...")
print("Registering voice CDR schema...")
voice_scehma_id = sr_client.register_schema("cdr.voice-value", cdr_voice_schema)
print("Registering SMS CDR schema...")
sms_scehma_id = sr_client.register_schema("cdr.sms-value", cdr_sms_schema)
print("Registering data CDR schema...")
data_scehma_id = sr_client.register_schema("cdr.data-value", cdr_data_schema)
print("Registering ok CDR schema...")
ok_scehma_id = sr_client.register_schema("cdr.ok-value", cdr_ok_schema)
print("Registering error CDR schema...")
error_scehma_id = sr_client.register_schema("cdr.error-value", cdr_error_schema)
print("Registering unratable CDR schema...")
unratable_scehma_id = sr_client.register_schema(
    "cdr.unratable-value", cdr_unratable_schema
)
print("Schemas registered successfully.")

cluster_metadata: ClusterMetadata = admin_client.list_topics()  # type: ignore

topics: Sequence[TopicMetadata] = cluster_metadata.topics.values()  # type: ignore

for topic in iter(topics):
    partitions: Sequence[PartitionMetadata] = topic.partitions.values()  # type: ignore
    if topic.topic.startswith("__"):  # type: ignore
        continue
    print(f"Topic: {topic.topic}, Partitions: {len(partitions)}")  # type: ignore
    for p in iter(partitions):  # type: ignore
        print(f"  Partition: {p.id}, Leader: {p.leader}")


print(f"Voice CDR schema ID: {voice_scehma_id}")
print(f"SMS CDR schema ID: {sms_scehma_id}")
print(f"Data CDR schema ID: {data_scehma_id}")
print(f"OK CDR schema ID: {ok_scehma_id}")
print(f"Error CDR schema ID: {error_scehma_id}")
print(f"Unratable CDR schema ID: {unratable_scehma_id}")
