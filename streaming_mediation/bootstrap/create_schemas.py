"""
This script is responsible for registering schemas with the Confluent Schema Registry.
"""

from confluent_kafka.schema_registry import SchemaRegistryClient, Schema  # type: ignore


sr_config = {
    "url": "http://localhost:8081",
}

sr_client = SchemaRegistryClient(sr_config)

with open("schemas/normalized_cdr.avsc", "r", encoding="utf-8") as f:
    ok_cdr_schema = f.read()

with open("schemas/normalized_cdr_error.avsc", "r", encoding="utf-8") as f:
    error_cdr_schema = f.read()

cdr_ok_schema = Schema(ok_cdr_schema, "AVRO")
cdr_error_schema = Schema(error_cdr_schema, "AVRO")
print("Registering schemas...")
print("Registering voice CDR schema...")
ok_scehma_id = sr_client.register_schema("cdr.ok-value", cdr_ok_schema)
print("Registering error CDR schema...")
error_schema_id = sr_client.register_schema("cdr.error-value", cdr_error_schema)
print("Schemas registered successfully.")

print(f"Voice CDR schema ID: {ok_scehma_id}")
print(f"Error CDR schema ID: {error_schema_id}")
