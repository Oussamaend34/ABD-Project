from typing import Sequence
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.admin import ClusterMetadata, TopicMetadata, PartitionMetadata
from confluent_kafka.schema_registry import SchemaRegistryClient, Schema
import os


def setup_kafka_topics_and_schemas(
    kafka_brokers: str = "localhost:9092,localhost:9093,localhost:9094",
    schema_registry_url: str = "http://localhost:8081",
    avro_dir: str = "avro",
):
    admin_config = {"bootstrap.servers": kafka_brokers}
    sr_config = {"url": schema_registry_url}

    admin_client = AdminClient(admin_config)
    sr_client = SchemaRegistryClient(sr_config)

    # Define topics
    topics = [
        NewTopic("cdr.voice", num_partitions=3, replication_factor=1),
        NewTopic("cdr.sms", num_partitions=3, replication_factor=1),
        NewTopic("cdr.data", num_partitions=3, replication_factor=1),
        NewTopic("cdr.ok", num_partitions=3, replication_factor=1),
        NewTopic("cdr.error", num_partitions=3, replication_factor=1),
        NewTopic("cdr.unratable", num_partitions=3, replication_factor=1),
        NewTopic("telecom.billing.invoice", num_partitions=3, replication_factor=1),
    ]

    print("Creating topics...")
    admin_client.create_topics(topics)

    # Load schemas from files
    schema_files = {
        "cdr.voice": "voice_cdr.avsc",
        "cdr.sms": "sms_cdr.avsc",
        "cdr.data": "data_edr.avsc",
        "cdr.ok": "normalized_cdr.avsc",
        "cdr.error": "normalized_cdr_error.avsc",
        "cdr.unratable": "unratable_cdr.avsc",
        "telecom.billing.invoice": "invoice.avsc",
    }

    schema_ids = {}

    print("Registering schemas...")
    for topic_name, filename in schema_files.items():
        path = os.path.join(avro_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            schema_str = f.read()

        schema = Schema(schema_str, "AVRO")
        subject = f"{topic_name}-value"
        schema_id = sr_client.register_schema(subject, schema)
        schema_ids[topic_name] = schema_id
        print(f"✅ Registered schema for topic `{topic_name}` with ID: {schema_id}")

    # Print created topics and partitions
    print("\nCluster topic information:")
    cluster_metadata: ClusterMetadata = admin_client.list_topics()
    topics_meta: Sequence[TopicMetadata] = cluster_metadata.topics.values()

    for topic in topics_meta:
        if topic.topic.startswith("__"):
            continue
        partitions: Sequence[PartitionMetadata] = topic.partitions.values()
        print(f"🟢 Topic: {topic.topic}, Partitions: {len(partitions)}")
        for p in partitions:
            print(f"  └ Partition: {p.id}, Leader: {p.leader}")

    # Final output
    print("\nSchema IDs:")
    for topic, sid in schema_ids.items():
        print(f"  {topic}: {sid}")


# Example call
if __name__ == "__main__":
    setup_kafka_topics_and_schemas()
