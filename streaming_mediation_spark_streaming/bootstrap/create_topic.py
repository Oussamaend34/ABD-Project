from typing import Sequence
from confluent_kafka.admin import AdminClient, NewTopic  # type: ignore
from confluent_kafka.admin import ClusterMetadata, TopicMetadata, PartitionMetadata  # type: ignore

admin_config = {
    "bootstrap.servers": "localhost:9092,localhost:9093,localhost:9094",
}

admin_client = AdminClient(admin_config)

ok_cdr_topic = NewTopic("cdr.ok", num_partitions=3, replication_factor=3)  # type: ignore
error_cdr_topic = NewTopic("cdr.error", num_partitions=3, replication_factor=3)  # type: ignore

topic_results = admin_client.create_topics(  # type: ignore
    [
        ok_cdr_topic,
        error_cdr_topic
    ]
)

cluster_metadata: ClusterMetadata = admin_client.list_topics()  # type: ignore

topics: Sequence[TopicMetadata] = cluster_metadata.topics.values()  # type: ignore

for topic in iter(topics):
    partitions: Sequence[PartitionMetadata] = topic.partitions.values()  # type: ignore
    print(f"Topic: {topic.topic}, Partitions: {len(partitions)}")  # type: ignore
    for p in iter(partitions):  # type: ignore
        print(f"  Partition: {p.id}, Leader: {p.leader}")  # type: ignore
