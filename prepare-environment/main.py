from register_connector import register_connector
from creating_topics_schemas import setup_kafka_topics_and_schemas
from populate_data import populate_database_from_csv_and_json
from register_tables_in_apache_pinot import register_tables_and_schemas


def main():
    """Main function to prepare the environment by registering the connector."""

    try:
        print("Setting up Kafka topics and schemas...")
        setup_kafka_topics_and_schemas()
    except Exception as e:
        print(f"❌ An error occurred while setting up Kafka topics and schemas: {e}")
    try:
        print("Registering the MongoDB sink connector...")
        register_connector(
            connector_config_json_path="mongodb_sink_connector_configuration.json"
        )
    except Exception as e:
        print(f"❌ An error occurred while registering the connector: {e}")
    try:
        print("Registering the database jdbc source connector...")
        register_connector(
            connector_config_json_path="jdbc-source-connector-config.json"
        )
    except Exception as e:
        print(f"❌ An error occurred while registering the connector: {e}")
    try:
        print("Registering Apache Pinot tables and schemas...")
        register_tables_and_schemas()
    except Exception as e:
        print(
            f"❌ An error occurred while registering Apache Pinot tables and schemas: {e}"
        )
    try:
        print("Populating the database from CSV and JSON files...")
        populate_database_from_csv_and_json()
    except Exception as e:
        print(f"❌ An error occurred while populating the database: {e}")


if __name__ == "__main__":
    print("Preparing environment...")
    main()
    print("Environment preparation complete.")
