import json
import requests


def register_connector(
    connector_config_json_path = "mongodb_sink_connector_configuration.json"
    ):
    """Register a connector with the Kafka Connect REST API using a JSON configuration file.
    Args:
        connector_config_json_path (str): Path to the JSON file containing the connector configuration.
    """
    with open(connector_config_json_path, "r") as f:
        config = json.load(f)

    connector_name = config.get("name")

    if not connector_name:
        raise ValueError("The JSON must contain a 'name' field.")

    url = f"http://localhost:8083/connectors/{connector_name}/config"

    response = requests.put(url, json=config, headers={"Content-Type": "application/json"})



    if response.ok:
        print(f"✅ Connector '{connector_name}' updated successfully.")
    else:
        print(f"❌ Failed to update connector '{connector_name}'.")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")


