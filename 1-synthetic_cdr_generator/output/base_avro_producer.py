"""
This file contains the base class for Avro producers.
"""

from typing import Dict, Any, Optional

from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField

from utils.schemas import CDR


class BaseAvroProducer:
    """
    Base class for Avro producers.
    """

    def __init__(
        self,
        producer: Producer,
        sr_client: SchemaRegistryClient,
        subject: str,
        topic: str,
    ):
        """
        Initialize the Avro producer.

        Args:
            producer (Producer): The Kafka producer instance.
            sr_client (SchemaRegistryClient): The Schema Registry client instance.
            subject (str): The subject name for the schema registry.
            topic (str): The topic name for the Kafka producer.
        """
        self.__producer = producer
        self.__sr_client = sr_client
        self.__subject = subject
        self.__topic = topic
        schema_response = sr_client.get_latest_version(self.__subject)
        self.schema_str = schema_response.schema.schema_str
        self.serializer = AvroSerializer(self.__sr_client, self.schema_str, self.__to_dict)

    def __to_dict(self, record: CDR, ctx: Any) -> Dict[str, Any]: # pylint: disable=unused-argument
        """
        Convert the CDR record to a dictionary.

        Args:
            record (CDR): The CDR record to convert.

        Returns:
            Dict[str, Any]: The dictionary representation of the CDR record.
        """
        return record.__dict__

    def produce(self, record: CDR) -> None:
        """
        Produce a record to the Kafka topic.
        Args:
            record (CDR): The CDR record to produce.
            key (Optional[str]): The key for the Kafka message.
            partition (Optional[int]): The partition for the Kafka message.
        """
        self.__producer.produce(
            topic=self.__topic,
            key=str(record.uuid),
            value=self.serializer(
                record, SerializationContext(self.__topic, MessageField.VALUE)
            ),
            on_delivery=self.__on_delivery,
        )
        self.__producer.poll(0)

    def __on_delivery(self, err: Optional[Exception], msg: Optional[Any]) -> None:
        """
        Callback function for message delivery.

        Args:
            err (Optional[Exception]): The error if any occurred during delivery.
            msg (Optional[Any]): The message that was delivered.
        """
        if err is not None:
            print(f"❌ Error Message delivery failed: {err}")
        else:
            print(f"✅ Message delivered to {msg.topic()} [{msg.partition()}]")

    def flush(self) -> None:
        """
        Flush the producer to ensure all messages are sent.
        """
        self.__producer.flush()
