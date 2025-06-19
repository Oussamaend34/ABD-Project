"""
    This module contains the schema definitions for various types of call detail records (CDRs).
"""
from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4


@dataclass
class CallerProfile:
    """
    Represents a caller profile with a unique MSISDN and location information.
    1. msisdn: Unique identifier for the caller.
    2. home_city: City where the caller is located.
    3. home_region: Region where the caller is located.
    """

    msisdn: str
    home_city: str
    home_region: str

@dataclass
class CDR(ABC):
    """
    Base class for Call Detail Records (CDRs).
    This class serves as a base for specific types of CDRs.
    """
@dataclass
class VoiceCDR(CDR):
    """
    Represents a voice call detail record (CDR) with relevant information.
    1. record_type: Type of the record (e.g., "Voice").
    2. timestamp: Timestamp of the record.
    3. caller_id: ID of the caller.
    4. callee_id: ID of the callee.
    5. duration_sec: Duration of the call in seconds.
    6. cell_id: ID of the cell tower used.
    7. technology: Technology used (e.g., "GSM", "UMTS").
    """
    record_type: str
    timestamp: datetime
    caller_id: str
    callee_id: str
    duration_sec: int
    cell_id: str
    technology: str
    uuid: str = uuid4().hex


@dataclass
class SMSCDR(CDR):
    """
    Represents a short message service (SMS) call detail record (CDR) with relevant information.
    1. record_type: Type of the record (e.g., "SMS").
    2. timestamp: Timestamp of the record.
    3. sender_id: ID of the sender.
    4. receiver_id: ID of the receiver.
    5. cell_id: ID of the cell tower used.
    6. technology: Technology used (e.g., "GSM", "UMTS").
    """
    record_type: str
    timestamp: datetime
    sender_id: str
    receiver_id: str
    cell_id: str
    technology: str
    uuid: str = uuid4().hex


@dataclass
class DataEDR(CDR):
    """
    Represents a data event detail record (EDR) with relevant information.
    1. record_type: Type of the record (e.g., "Data").
    2. timestamp: Timestamp of the record.
    3. user_id: ID of the user.
    4. data_volume_mb: Volume of data used in megabytes.
    5. session_duration_sec: Duration of the session in seconds.
    6. cell_id: ID of the cell tower used.
    7. technology: Technology used (e.g., "GPRS", "LTE").
    """
    record_type: str
    timestamp: datetime
    user_id: str
    data_volume_mb: float
    session_duration_sec: int
    cell_id: str
    technology: str
    uuid: str = uuid4().hex
