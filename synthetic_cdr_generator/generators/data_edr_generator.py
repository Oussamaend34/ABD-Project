"""
This module defines the DataEDRGenerator class,
    which is responsible for generating synthetic Data EDRs (Event Data Records).
"""

from typing import List, Dict, Optional, Sequence
from datetime import datetime
from uuid import uuid4

from utils import load_geography, get_duration_data_usage_to_technology
from utils.schemas import DataEDR, CallerProfile
from .base_generator import BaseGenerator


class DataEDRGenerator(BaseGenerator):
    """
    This class generates synthetic data event detail records (EDRs).
    """

    def __init__(
        self,
        caller_pool: List[CallerProfile],
        cities_data: Dict[str, Dict[str, str]] = load_geography(),
        technologies: Optional[Dict[str, float]] = None,
    ):
        """
        Initialize the VoiceCDRGenerator with a caller pool, geography data,
            error injector, and configuration.
        """
        if technologies is None:
            technologies = {"2G": 0.05, "3G": 0.1, "4G": 0.6, "5G": 0.25}
        super().__init__(caller_pool, cities_data, technologies)
        self.record_type = "data"

    def generate(self) -> DataEDR:
        """
        Generate a single synthetic data event detail record (EDR).
        Returns:
            DataEDR: A synthetic data EDR.
        """
        user_id: CallerProfile = self._get_random_caller()
        technology: str = self._get_technology()
        duration, data_volume = get_duration_data_usage_to_technology(
            technology=technology
        )
        return DataEDR(
            record_type=self.record_type,
            timestamp=datetime.now(),
            user_id=user_id.msisdn,
            data_volume_mb=data_volume,
            cell_id=self._pick_cell_id(caller=user_id),
            session_duration_sec=duration,
            technology=technology,
            uuid=uuid4().hex,
        )

    def generate_batch(self, batch_size: int) -> Sequence[DataEDR]:
        """
        Generate a batch of synthetic data event detail records (EDRs).
        Args:
            batch_size (int): The number of EDRs to generate.
        Returns:
            Sequence[DataEDR]: A list of synthetic data EDRs.
        """
        return [self.generate() for _ in range(batch_size)]
