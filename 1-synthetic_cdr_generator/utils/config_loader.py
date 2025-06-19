"""
This file contains the configuration loader for the synthetic CDR generator.
"""

from pprint import pprint
from copy import deepcopy
import yaml


def load_config(path="config/config.yaml") -> dict:
    """
    Load the configuration file.
    """
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_generator_config(config=load_config()):
    """
    Load the generator configuration.
    Args:
        config (dict): The configuration dictionary.

    Returns:
        dict: The generator configuration.
    """
    return config["generation"]

def load_files_config(config=load_config()):
    """
    Load the file configuration.
    Args:
        config (dict): The configuration dictionary.

    Returns:
        dict: The file configuration.
    """
    return config["files"]

def load_kafka_producer_config(config=load_config()):
    """
    Load the Kafka producer configuration.
    Args:
        config (dict): The configuration dictionary.

    Returns:
        dict: The Kafka producer configuration.
    """
    return config["kafka"]


def load_schema_registry_config(config=load_config()):
    """
    Load the Schema Registry configuration.
    Args:
        config (dict): The configuration dictionary.

    Returns:
        dict: The Schema Registry configuration.
    """
    return config["schema_registry"]


def load_topics_config(config=load_config()):
    """
    Load the topic configuration.
    Args:
        config (dict): The configuration dictionary.

    Returns:
        dict: The topic configuration.
    """
    return config["topics"]


def load_subjects_config(config=load_config()):
    """
    Load the subject configuration.
    Args:
        config (dict): The configuration dictionary.

    Returns:
        dict: The subject configuration.
    """
    return config["subjects"]


def load_technologies_config(config=load_config()):
    """
    Load the technology configuration.
    Args:
        config (dict): The configuration dictionary.

    Returns:
        dict: The technology configuration.
    """
    return config["technologies"]


def load_call_duration_config(config=load_config()):
    """
    Load the call duration configuration.
    Args:
        config (dict): The configuration dictionary.

    Returns:
        dict: The call duration configuration.
    """
    return config["call_duration"]


def load_data_duration_usage_config(config=load_config()):
    """
    Load the data usage configuration.
    Args:
        config (dict): The configuration dictionary.

    Returns:
        dict: The data usage configuration.
    """
    config_copy = deepcopy(config)
    data_duration_usage = config_copy["data_duration_usage"]
    data_duration_usage["default"] = (
        data_duration_usage["default"]["mean"],
        data_duration_usage["default"]["sigma"],
    )
    for technology in data_duration_usage["overrides"]:
        data_duration_usage["overrides"][technology] = (
            data_duration_usage["overrides"][technology]["mean"],
            data_duration_usage["overrides"][technology]["sigma"],
        )
    return data_duration_usage

def load_data_speed_config(config=load_config()):
    """
    Load the data speed configuration.
    Args:
        config (dict): The configuration dictionary.

    Returns:
        dict: The data speed configuration.
    """
    config_copy = deepcopy(config)
    data_speed = config_copy["data_speed"]
    data_speed["default"] = (
        data_speed["default"]["mean"],
        data_speed["default"]["sigma"],
    )
    for technology in data_speed["overrides"]:
        data_speed["overrides"][technology] = (
            data_speed["overrides"][technology]["mean"],
            data_speed["overrides"][technology]["sigma"],
        )
    return data_speed
def load_errors_config(config=load_config()):
    """
    Load the error configuration.
    Args:
        config (dict): The configuration dictionary.

    Returns:
        dict: The error configuration.
    """
    return config["errors"]


if __name__ == "__main__":
    _config = load_config()
    pprint(_config)
    pprint(load_data_duration_usage_config(_config))
