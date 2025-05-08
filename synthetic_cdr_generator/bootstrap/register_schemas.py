"""
This script is responsible for registering schemas with the Confluent Schema Registry.
"""

from confluent_kafka.schema_registry import SchemaRegistryClient, Schema  # type: ignore


sr_config = {
    "url": "http://localhost:8081",
}

sr_client = SchemaRegistryClient(sr_config)

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

cdr_voice_schema = Schema(voice_cdr_schema, "AVRO")
cdr_sms_schema = Schema(sms_cdr_schema, "AVRO")
cdr_data_schema = Schema(data_edr_schema, "AVRO")
cdr_ok_schema = Schema(ok_cdr_schema, "AVRO")
cdr_error_schema = Schema(error_cdr_schema, "AVRO")

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
print("Schemas registered successfully.")

print(f"Voice CDR schema ID: {voice_scehma_id}")
print(f"SMS CDR schema ID: {sms_scehma_id}")
print(f"Data CDR schema ID: {data_scehma_id}")
print(f"OK CDR schema ID: {ok_scehma_id}")
print(f"Error CDR schema ID: {error_scehma_id}")
