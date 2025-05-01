"""
This module contains helper functions for the synthetic CDR generator.
"""

from typing import List, Optional, Dict
import random
from dataclasses import dataclass
import json


@dataclass
class CallerProfile:
    """
    Represents a caller profile with a unique MSISDN and location information.
    """

    msisdn: str
    home_city: str
    home_region: str


def generate_msisdn() -> str:
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
    with open("./utils/cities.json", "r", encoding="utf-8") as f:
        cities = json.load(f)
    with open("./utils/regions.json", "r", encoding="utf-8") as f:
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
            msisdn=generate_msisdn(),
            home_city=home_city,
            home_region=home_region,
        )
        pool.append(caller_profile)
    return pool


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


if __name__ == "__main__":
    _cities = load_geography()
    _pool = init_pool(100, cities=_cities)
    _caller = get_random_caller(_pool)
    _callee = get_random_callee(_pool, exclude=_caller)
    print(f"Caller: {_caller}")
    print(f"Callee: {_callee}")
