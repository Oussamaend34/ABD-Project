"""
This is a utility module to register Apache Pinot schemas and table configs via REST API.
"""

import os
import json
import requests
import sys


PINOT_CONTROLLER_URL = "http://localhost:9000"
CONFIG_FOLDER = "apache_pinot"

# Map files to their corresponding API endpoints
FILES = {
    "normalized_cdr_schema.json": f"{PINOT_CONTROLLER_URL}/schemas",
    "normalized_error_cdr_schema.json": f"{PINOT_CONTROLLER_URL}/schemas",
    "normalized_cdr_table.json": f"{PINOT_CONTROLLER_URL}/tables",
    "normalized_error_cdr_table.json": f"{PINOT_CONTROLLER_URL}/tables",
}


def post_config(file_path, endpoint_url, config_folder= CONFIG_FOLDER):
    """
    Send a POST request to Pinot Controller with the provided JSON file.
    """
    path = os.path.join(config_folder, file_path)
    with open(path, "r") as f:
        payload = json.load(f)

    response = requests.post(
        endpoint_url,
        headers={"Content-Type": "application/json"},
        json=payload
    )

    if response.status_code == 200:
        print(f"✅ Successfully registered {file_path} to {endpoint_url}")
    else:
        print(f"❌ Failed to register {file_path}")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        sys.exit(1)


def register_tables_and_schemas():
    for file_name, endpoint_url in FILES.items():
        print(f"📦 Registering {file_name}...")
        post_config(file_name, endpoint_url)


if __name__ == "__main__":
    register_tables_and_schemas()
