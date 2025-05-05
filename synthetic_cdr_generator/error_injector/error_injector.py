"""
This module contains the error injector class for the synthetic CDR generator.
"""

from typing import Dict, Optional, Any, Tuple, Sequence, List, TypeVar
from datetime import datetime
import copy
import random

from utils.schemas import CDR

T = TypeVar("T", bound=CDR)


class ErrorInjector:
    """
    This class is responsible for injecting errors into the generated CDRs.
    """

    def __init__(
        self, error_rate: float = 0.1, error_types: Optional[Dict[str, float]] = None
    ):
        """
        Initialize the ErrorInjector with a specified error rate.

        Args:
            error_rate (float): The probability of injecting an error into a CDR.
        """
        self.error_rate = error_rate
        self.error_types = error_types or {
            "missing_field": 0.4,
            "negative_value": 0.2,
            "invalid_type": 0.2,
            "out_of_order_timestamp": 0.1,
            "duplicate": 0.1,
        }

    def inject(self, record: T) -> Tuple[T, Optional[str]]:
        """
        Inject an error into the given record based on the specified error rate.
        Args:
            record (Dict[str, Any]): The record to inject an error into.
        Returns:
            Dict[str, Any]: The record with the injected error.
        """
        if random.random() > self.error_rate:
            return record, None

        record_dict = copy.deepcopy(record.__dict__)
        error_type = self._choose_error_type()
        if error_type == "missing_field":
            self._inject_missing_field(record_dict)
        elif error_type == "negative_value":
            self._inject_negative_value(record_dict)
        elif error_type == "invalid_type":
            self._inject_invalid_type(record_dict)

        elif error_type == "out_of_order_timestamp":
            self._inject_old_timestamp(record_dict)

        record = type(record)(**record_dict)
        return record, error_type

    def inject_batch(self, records: Sequence[CDR]) -> List[Tuple[CDR, Optional[str]]]:
        """
        Inject errors into a batch of records.
        Args:
            records (Sequence[CDR]): The records to inject errors into.
        Returns:
            List[Tuple[CDR, str]]: A list of tuples containing the record and the error type.
        """
        return [self.inject(record) for record in records]

    def _choose_error_type(self) -> str:
        types = list(self.error_types.keys())
        weights = list(self.error_types.values())
        return random.choices(types, weights=weights, k=1)[0]

    def _inject_missing_field(self, record: Dict[str, Any]):
        # Protect required fields for Avro
        protected = [
            "record_type",
            "uuid",
        ]
        keys = [k for k in record if k not in protected]
        if keys:
            field = random.choice(keys)
            if isinstance(record[field], str):
                record[field] = ""
            elif isinstance(record[field], (int, float)):
                record[field] = -9999
            else:
                record[field] = "?"

    def _inject_negative_value(self, record: Dict[str, Any]):
        keys = list(record.keys())
        keys = [k for k in keys if isinstance(record[k], (int, float))]
        if not keys:
            return
        field = random.choice(keys)
        record[field] = -abs(record[field])

    def _inject_invalid_type(self, record: Dict[str, Any]):
        protected = [
            "record_type",
            "uuid",
            "timestamp",
            "caller_id",
            "sender_id",
            "user_id",
        ]
        keys = [k for k in record if k not in protected]
        if not keys:
            return

        key = random.choice(keys)
        value = record[key]

        # Corrupt without changing type class
        if isinstance(value, (int, float)):
            record[key] = -9999
        elif isinstance(value, str):
            record[key] = "INVALID!@#"

    def _inject_old_timestamp(self, record: Dict[str, Any]):
        if "timestamp" in record:
            record["timestamp"] = datetime(
                random.randint(1970, 2020),
                random.randint(1, 12),
                random.randint(1, 28),
                random.randint(0, 23),
                random.randint(0, 59),
                random.randint(0, 59),
            )
