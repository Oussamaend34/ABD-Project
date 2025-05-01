"""
This module generates a synthetic SMS CDR (Call Detail Record) dataset.
"""

from typing import List, Dict, Optional, Sequence
from datetime import datetime


from utils import load_geography
from utils.schemas import SMSCDR, CallerProfile
from error_injector import ErrorInjector
from .base_generator import BaseGenerator


class SMSCDRGenerator(BaseGenerator):
    """
    This class generates synthetic SMS call detail records (CDRs).
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
        self.record_type = "sms"

    def generate(self) -> SMSCDR:
        """
        Generate a single synthetic SMS call detail record (CDR).
        Returns:
            SMSCDR: A synthetic SMS CDR.
        """
        sender: CallerProfile = self._get_random_caller()
        receiver: CallerProfile = self._get_random_callee(sender)
        technology: str = self._get_technology()
        return SMSCDR(
            record_type=self.record_type,
            timestamp=datetime.now(),
            sender_id=sender.msisdn,
            receiver_id=receiver.msisdn,
            cell_id=self._pick_cell_id(caller=sender),
            technology=technology,
        )

    def generate_batch(self, batch_size: int) -> Sequence[SMSCDR]:
        """
        Generate a batch of synthetic SMS call detail records (CDRs).
        Args:
            batch_size (int): The number of CDRs to generate.
        Returns:
            Sequence[SMSCDR]: A list of synthetic SMS CDRs.
        """
        return [self.generate() for _ in range(batch_size)]
