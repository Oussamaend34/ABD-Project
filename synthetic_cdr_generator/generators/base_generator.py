"""
This module contains the base class for all generators.
"""

from typing import List, Dict, Optional, Union, Sequence
import random
from abc import ABC, abstractmethod
from utils import (
    get_random_caller,
    get_random_callee,
    load_geography,
    pick_location,
    pick_cell_id
)
from utils.schemas import VoiceCDR, SMSCDR, DataEDR, CallerProfile
from error_injector import ErrorInjector


class BaseGenerator(ABC):
    """
    Base class for all generators.
    """

    def __init__(
        self,
        caller_pool: List[CallerProfile],
        cities_data: Dict[str, Dict[str, str]] = load_geography(),
        technologies: Optional[Dict[str,float]] = None,
        error_injector: Optional[ErrorInjector] = None,
        config: Optional[Dict[str, str]] = None,
    ):
        self.caller_pool = caller_pool
        self.cities = cities_data
        self.technologies = technologies if technologies is not None else {}
        self.error_injector = error_injector
        self.config = config if config is not None else {}

    @abstractmethod
    def generate(self) -> Union[VoiceCDR, SMSCDR, DataEDR]:
        """
        Generate a single synthetic record.
        """

    @abstractmethod
    def generate_batch(self, batch_size: int) -> Sequence[Union[VoiceCDR, SMSCDR, DataEDR]]:
        """
        Generate a batch of synthetic records.
        """

    def _get_random_caller(self) -> CallerProfile:
        """
        Get a random caller from the pool.
        """
        return pick_location(get_random_caller(self.caller_pool))

    def _get_random_callee(self, caller: CallerProfile) -> CallerProfile:
        """
        Get a random callee from the pool, excluding the caller.
        """
        return pick_location(get_random_callee(self.caller_pool, caller))

    def _pick_cell_id(self, caller: CallerProfile) -> str:
        """
        Pick a cell ID based on the caller's location.
        """
        return pick_cell_id(caller, self.cities)
    
    def _get_technology(self) -> str:
        """
        Get a random technology from the list of technologies.
        """
        technologies = list(self.technologies.keys())
        probabilities = list(self.technologies.values())
        return random.choices(technologies, weights=probabilities, k=1)[0]
