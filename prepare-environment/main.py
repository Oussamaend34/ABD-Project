from register_connector import register_connector
from creating_topics_schemas import setup_kafka_topics_and_schemas
from populate_data import populate_database_from_csv_and_json



def main():
    """Main function to prepare the environment by registering the connector."""

    
    try:
        print("Setting up Kafka topics and schemas...")
        setup_kafka_topics_and_schemas()
    except Exception as e:
        print(f"❌ An error occurred while setting up Kafka topics and schemas: {e}")
    try:
        print("Registering the MongoDB sink connector...")
        register_connector()
    except Exception as e:
        print(f"❌ An error occurred while registering the connector: {e}")
    try:
        print("Populating the database from CSV and JSON files...")
        populate_database_from_csv_and_json()
    except Exception as e:
        print(f"❌ An error occurred while populating the database: {e}")
    
if __name__ == "__main__":
    print("Preparing environment...")
    main()
    print("Environment preparation complete.")