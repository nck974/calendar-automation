from typing import TypedDict


class Event(TypedDict):
    """
    Model of the required data to create an event
    """
    name: str
    description: str
    start_datetime: str
    duration_minutes: int
