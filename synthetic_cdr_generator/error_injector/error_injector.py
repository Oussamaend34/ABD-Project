"""
    This module contains the error injector class for the synthetic CDR generator.
"""

class ErrorInjector:
    """
    This class is responsible for injecting errors into the generated CDRs.
    """

    def __init__(self, error_rate: float = 0.1):
        """
        Initialize the ErrorInjector with a specified error rate.

        Args:
            error_rate (float): The probability of injecting an error into a CDR.
        """
        self.error_rate = error_rate
