"""
This module defines the VoiceCDRGenerator class,
    which is responsible for generating synthetic voice call detail records (CDRs).
"""

from typing import List, Dict, Optional, Sequence
from datetime import datetime

from utils import load_geography, get_duration_corresponding_to_technology
from utils.schemas import VoiceCDR, CallerProfile
from error_injector import ErrorInjector
from .base_generator import BaseGenerator


class VoiceCDRGenerator(BaseGenerator):
    """
    This class generates synthetic voice call detail records (CDRs).
    """

    def __init__(
        self,
        caller_pool: List[CallerProfile],
        cities_data: Dict[str, Dict[str, str]] = load_geography(),
        technologies: Optional[Dict[str, float]] = None,
        error_injector: Optional[ErrorInjector] = None,
        config: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize the VoiceCDRGenerator with a caller pool, geography data,
            error injector, and configuration.
        """
        if technologies is None:
            technologies = {"2G": 0.05, "3G": 0.1, "4G": 0.6, "5G": 0.25}
        super().__init__(caller_pool, cities_data, technologies, error_injector, config)
        self.record_type = "voice"

    def generate(self) -> VoiceCDR:
        """
        Generate a single synthetic voice call detail record (CDR).
        Returns:
            VoiceCDR: A synthetic voice CDR.
        """
        caller: CallerProfile = self._get_random_caller()
        callee: CallerProfile = self._get_random_callee(caller)
        technology: str = self._get_technology()
        return VoiceCDR(
            record_type=self.record_type,
            caller_id=caller.msisdn,
            timestamp=datetime.now(),
            callee_id=callee.msisdn,
            duration_sec=get_duration_corresponding_to_technology(
                technology=technology
            ),
            cell_id=self._pick_cell_id(caller=caller),
            technology=technology,
        )

    def generate_batch(self, batch_size: int) -> Sequence[VoiceCDR]:
        """
        Generate a batch of synthetic voice call detail records (CDRs).
        Args:
            batch_size (int): The number of records to generate.
        
        Returns:
            List[VoiceCDR]: A list of synthetic voice CDRs.
        """
        return [self.generate() for _ in range(batch_size)]
