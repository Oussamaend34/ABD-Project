"""
This module contains the base class for all generators.
"""

from abc import ABC, abstractmethod


class BaseGenerator(ABC):
    """
    Base class for all generators.
    """

    @abstractmethod
    def generate(self):
        """
        Generate a single synthetic record.
        """

    @abstractmethod
    def generate_batch(self, batch_size: int):
        """
        Generate a batch of synthetic records.
        """
