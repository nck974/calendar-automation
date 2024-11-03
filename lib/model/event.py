from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:
    """
    Model of the required data to create an event
    """
    name: str
    description: str
    start_datetime: datetime
    duration_minutes: int
