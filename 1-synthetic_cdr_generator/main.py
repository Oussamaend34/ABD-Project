"""
This is a test file.
"""

import time
import random


from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient

from utils import (
    init_pool,
    load_caller_profiles,
    load_geography,
    load_config,
    load_generator_config,
    load_errors_config,
    load_kafka_producer_config,
    load_schema_registry_config,
    load_topics_config,
    load_subjects_config,
    load_technologies_config,
)

# from utils.schemas import CDR
from error_injector.error_injector import ErrorInjector
from generators import VoiceCDRGenerator, SMSCDRGenerator, DataEDRGenerator

from output import BaseAvroProducer

if __name__ == "__main__":
    CONFIG = load_config()
    GENERATOR_CONFIG = load_generator_config(CONFIG)
    ERROR_CONFIG = load_errors_config(CONFIG)
    TOPICS = load_topics_config(CONFIG)
    SUBJECTS = load_subjects_config(CONFIG)
    CITIES_DATA = load_geography()
    TECHNOLOGIES = load_technologies_config(CONFIG)
    SR_CONFIG = load_schema_registry_config(CONFIG)
    PRODUCER_CONFIG = load_kafka_producer_config(CONFIG)

    SCHEMA_REGISTRY_CLIENT = SchemaRegistryClient(SR_CONFIG)
    PRODUCER = Producer(PRODUCER_CONFIG)

    RECORDS_PER_HOUR = GENERATOR_CONFIG["records_per_hour"]
    CUSTOMER_CSV_FILE = GENERATOR_CONFIG["customer_csv_file"]
    SEED = GENERATOR_CONFIG["seed"]
    VOICE_TOPIC = TOPICS["voice"]
    VOICE_SUBJECT = SUBJECTS["voice"]
    SMS_TOPIC = TOPICS["sms"]
    SMS_SUBJECT = SUBJECTS["sms"]
    DATA_TOPIC = TOPICS["data"]
    DATA_SUBJECT = SUBJECTS["data"]
    ERROR_ENABLED = ERROR_CONFIG["enabled"]
    ERROR_RATE = ERROR_CONFIG["rate"]
    ERROR_TYPES = ERROR_CONFIG["types"]
    CDR_DISTRIBUTION = GENERATOR_CONFIG["distribution"]

    msisdn_pool = load_caller_profiles(CUSTOMER_CSV_FILE)

    voice_generator = VoiceCDRGenerator(
        caller_pool=msisdn_pool, cities_data=CITIES_DATA, technologies=TECHNOLOGIES
    )
    sms_generator = SMSCDRGenerator(
        caller_pool=msisdn_pool, cities_data=CITIES_DATA, technologies=TECHNOLOGIES
    )
    data_generator = DataEDRGenerator(
        caller_pool=msisdn_pool, cities_data=CITIES_DATA, technologies=TECHNOLOGIES
    )
    injector = ErrorInjector(error_rate=ERROR_RATE, error_types=ERROR_TYPES)

    voice_avro_producer = BaseAvroProducer(
        producer=PRODUCER,
        sr_client=SCHEMA_REGISTRY_CLIENT,
        topic=VOICE_TOPIC,
        subject=VOICE_SUBJECT,
    )
    sms_avro_producer = BaseAvroProducer(
        producer=PRODUCER,
        sr_client=SCHEMA_REGISTRY_CLIENT,
        topic=SMS_TOPIC,
        subject=SMS_SUBJECT,
    )
    data_avro_producer = BaseAvroProducer(
        producer=PRODUCER,
        sr_client=SCHEMA_REGISTRY_CLIENT,
        topic=DATA_TOPIC,
        subject=DATA_SUBJECT,
    )

    seconds_between_records = 3600 / RECORDS_PER_HOUR
    types = list(CDR_DISTRIBUTION.keys())
    weights = list(CDR_DISTRIBUTION.values())

    print(
        f"📡 Starting continuous CDR generation at {RECORDS_PER_HOUR} records/hour..."
    )
    try:
        while True:
            record_type = random.choices(types, weights=weights, k=1)[0]

            # Generate
            if record_type == "voice":
                record = voice_generator.generate()
            elif record_type == "sms":
                record = sms_generator.generate()
            elif record_type == "data":
                record = data_generator.generate()
            else:
                continue

            # Inject errors
            if ERROR_ENABLED:
                record, error_type = injector.inject(record)
                if error_type:
                    print(f"💥 Injected error: {error_type}")
            # Send
            try:
                print(f"📤 Sending {record_type} record: {record.uuid}")
                if record_type == "voice":
                    voice_avro_producer.produce(record=record)
                elif record_type == "sms":
                    sms_avro_producer.produce(record=record)
                elif record_type == "data":
                    data_avro_producer.produce(record=record)
            except Exception as e:  # pylint: disable=broad-except
                print(f"❌ Error sending {record_type} record: {e}")

            # Throttle
            time.sleep(seconds_between_records)

    except KeyboardInterrupt:
        print("\n🛑 Stopping gracefully...")

    # Flush all producers
    voice_avro_producer.flush()
    sms_avro_producer.flush()
    data_avro_producer.flush()

    print("✅ Producers flushed. Goodbye.")
