"""
This module contains helper functions for data processing.
"""

import re
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

def __normalize_msisdn(msisdn: str) -> str:
    """
    Normalize Moroccan MSISDN:
    - Remove spaces, dashes, parentheses, etc.
    - Convert local format (06/07) to international (2126/2127)
    """
    if msisdn is None:
        return None
    digits = re.sub(r"\D", "", msisdn)

    if digits.startswith("06") or digits.startswith("07"):
        digits = "212" + digits[1:]
    elif digits.startswith("00212"):
        digits = digits[2:]
    elif digits.startswith("212"):
        pass
    elif digits.startswith("+212"):
        digits = digits[1:]

    return digits if digits.startswith("212") else None

normalize_msisdn_udf = udf(__normalize_msisdn, StringType())
