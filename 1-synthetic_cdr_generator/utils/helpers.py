"""
This module contains helper functions for the synthetic CDR generator.
"""

from typing import List, Optional, Dict, Tuple
import random
import json
import csv

import numpy as np

from .schemas import CallerProfile
from .config_loader import (
    load_config,
    load_call_duration_config,
    load_data_duration_usage_config,
    load_data_speed_config,
    load_files_config,
)


CONFIG = load_config()


def _generate_msisdn() -> str:
    """
    Generate a random MSISDN (Mobile Station International Subscriber Directory Number).
    The MSISDN is a unique number used to identify a mobile phone number.
    The format is typically 2126XXXXXXXX or 2127XXXXXXXX.

    Returns:
        str: A randomly generated MSISDN.
    """
    prefix = random.choice(["2126", "2127"])
    number = random.randint(10000000, 99999999)
    return f"{prefix}{number}"


def load_geography() -> Dict[str, Dict[str, str]]:
    """
    Load geography data from a CSV file.

    Returns:
        Dict[str, Dict[str, str]]: A dictionary mapping city names to their regions and countries.
    """
    files = load_files_config(CONFIG)
    cities_file = files.get("cities")
    regions_file = files.get("regions")
    with open(cities_file, "r", encoding="utf-8") as f:
        cities = json.load(f)
    with open(regions_file, "r", encoding="utf-8") as f:
        regions = json.load(f)
    regions_map = {key: value["name"] for key, value in regions.items()}
    for city in cities:
        cities[city]["region_name"] = regions_map.get(
            cities[city]["region_id"], "Unknown"
        )
    return cities


def init_pool(
    pool_size: int = 10000,
    seed: Optional[int] = None,
    cities: Dict[str, Dict[str, str]] = load_geography(),
) -> List[CallerProfile]:
    """
    Initialize a pool of random MSISDNs.

    Args:
        pool_size (int): The size of the pool to generate.
        seed (Optional[int]): Optional seed for random number generation.

    Returns:
        List[CallerProfile]: A list of randomly generated MSISDNs.
    """
    if seed is not None:
        random.seed(seed)
    pool: List[CallerProfile] = []
    for _ in range(pool_size):
        home_city_key = random.choice(list(cities.keys()))
        home_city = cities[home_city_key]["name"]
        home_region = cities[home_city_key]["region_name"]
        caller_profile = CallerProfile(
            msisdn=_generate_msisdn(),
            home_city=home_city,
            home_region=home_region,
        )
        pool.append(caller_profile)
    return pool

def load_caller_profiles(csv_file_path: str) -> list[CallerProfile]:
    caller_profiles = []
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            profile = CallerProfile(
                msisdn=row['msisdn'],
                home_city=row['home_city_name'],
                home_region=row['home_region_name']
            )
            caller_profiles.append(profile)
    return caller_profiles

def get_random_caller(pool: List[CallerProfile]) -> CallerProfile:
    """
    Get a random caller from the pool.

    Args:
        pool (List[CallerProfile]): The pool of MSISDNs to choose from.

    Returns:
        CallerProfile: A random MSISDN from the pool.
    """
    return random.choice(pool)


def get_random_callee(
    pool: List[CallerProfile], exclude: CallerProfile
) -> CallerProfile:
    """
    Get a random callee from the pool, excluding the specified number.

    Args:
        pool (List[CallerProfile]): The pool of MSISDNs to choose from.
        exclude (CallerProfile): The MSISDN to exclude from the pool.

    Returns:
        CallerProfile: A random MSISDN from the pool, excluding the specified number.
    """
    while True:
        candidate = random.choice(pool)
        if candidate.msisdn != exclude.msisdn:
            return candidate


def pick_location(
    caller: CallerProfile,
    cities: Dict[str, Dict[str, str]] = load_geography(),
    home_prob: float = 0.85,
) -> CallerProfile:
    """
    Pick a random location from the pool, excluding the specified number.

    Args:
        pool (List[CallerProfile]): The pool of MSISDNs to choose from.
        caller (CallerProfile): The MSISDN to pick the location for.

    Returns:
        CallerProfile: A random location from the pool, excluding the specified number.
    """
    if random.random() < home_prob:
        return caller
    else:
        other_cities = [
            key for key, c in cities.items() if c["name"] != caller.home_city
        ]
        other_city_key = random.choice(other_cities)
        other_city = cities[other_city_key]["name"]
        return CallerProfile(
            msisdn=caller.msisdn,
            home_city=other_city,
            home_region=cities[other_city_key]["region_name"],
        )


def pick_cell_id(
    caller: CallerProfile,
    cities: Dict[str, Dict[str, str]] = load_geography(),
) -> str:
    """
    Pick a random cell ID from the pool.

    Args:
        pool (List[CallerProfile]): The pool of MSISDNs to choose from.
        caller (CallerProfile): The MSISDN to pick the location for.

    Returns:
        str: A random cell ID from the pool.
    """
    number = random.randint(1, 100)
    for _, city in cities.items():
        if city["name"] == caller.home_city:
            number = random.randint(1, int(city["max_cell_id"]))
            return f"{city['pretty_name']}_{number}"
    return f"{caller.home_city}_{number}"


def get_duration_corresponding_to_technology(technology: str) -> int:
    """
    Get the duration corresponding to the technology.

    Args:
        technology (str): The technology to get the duration for.

    Returns:
        int: The duration corresponding to the technology.
    """
    config = load_call_duration_config(CONFIG)
    tech_scaling = config["technologies"]
    scale = tech_scaling.get(technology, config["default"])

    # Adjusted parameters to generate realistic duration
    base_duration = np.random.lognormal(
        mean=config["distribution"]["mean"], sigma=config["distribution"]["sigma"]
    )
    duration = base_duration * 60 * scale

    return int(min(duration, config["max"]))


def get_duration_data_usage_to_technology(technology: str) -> Tuple[int, float]:
    """
    Get the duration and data volume corresponding to the technology.

    Args:
        technology (str): The technology to get the duration and data volume for.

    Returns:
        Tuple[int, float]: The duration and data volume corresponding to the technology.
    """

    config_duration = load_data_duration_usage_config(CONFIG)
    config_speed = load_data_speed_config(CONFIG)

    tech_duration_norm = config_duration["overrides"]

    tech_speed_norm = config_speed["overrides"]

    mean_dur, std_dur = tech_duration_norm.get(
        technology,
        (config_duration["default"][0], config_duration["default"][1]),
    )
    duration = max(1, int(random.gauss(mean_dur, std_dur)))
    duration = min(duration, 2 * 3600)  # cap at 2 hours

    mean_speed, std_speed = tech_speed_norm.get(
        technology, (config_speed["default"][0], config_speed["default"][1])
    )
    speed = max(0.01, random.gauss(mean_speed, std_speed))

    volume_bits = speed * 1_000_000 * duration
    volume_mb = volume_bits / (8 * 1_000_000)

    return duration, round(volume_mb, 2)


if __name__ == "__main__":
    _cities = load_geography()
    _pool = init_pool(100, cities=_cities)
    _caller = get_random_caller(_pool)
    _callee = get_random_callee(_pool, exclude=_caller)
    print(f"Caller: {_caller}")
    print(f"Callee: {_callee}")
