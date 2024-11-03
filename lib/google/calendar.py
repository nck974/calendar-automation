"""
Module to manage the calendars
"""

from datetime import datetime, timedelta
import os
from typing_extensions import Final
from googleapiclient.discovery import build

from lib.environment import Env
from lib.exceptions.resource_not_found import ResourceNotFoundException
from lib.google.oauth2 import get_credentials
from lib.google.typing.calendars import (
    CalendarListEntry,
    CalendarListResponse,
    CalendarService,
)
from lib.google.typing.events import EventInput, EventsResponse
from lib.model.event import Event


class GoogleCalendar:
    """
    Manage API calls to the Google calendar API
    """

    # Configure the maximum pages that will be searched
    MAX_PAGES: Final[int] = int(
        os.environ.get(Env.MAX_SEARCH_CALENDAR_PAGES.value) or 10
    )
    TIME_ZONE: Final = os.environ.get(Env.TIME_ZONE.value) or "Europe/Berlin"

    service: CalendarService

    def __init__(self):
        """ """
        self.get_service()

    def get_service(self) -> None:
        """
        Login to the api
        """
        self.service = build("calendar", "v3", credentials=get_credentials())

    def get_calendars(self) -> list[CalendarListEntry]:
        """
        Return the list of available calendars
        """
        page_token = None
        calendars: list[CalendarListEntry] = []
        for _ in range(self.MAX_PAGES):
            calendar_response: CalendarListResponse = (
                self.service.calendarList().list(pageToken=page_token).execute()
            )
            if "items" in calendar_response:
                calendars = calendars + calendar_response["items"]

            page_token = calendar_response.get("nextPageToken")
            if not page_token:
                break

        return calendars

    def get_calendar_by_name(self, name: str) -> CalendarListEntry:
        """
        Return the given calendar by name
        """
        calendars = self.get_calendars()
        for calendar in calendars:
            if calendar["summary"] == name.strip():
                return calendar

        raise ResourceNotFoundException

    @classmethod
    def _generate_event(cls, event: Event) -> EventInput:
        """
        Return the event input object expected by the google
        """
        start_datetime = datetime.fromisoformat(event["start_datetime"])

        return {
            "summary": event["name"],
            "description": event.get("description"),
            "start": {
                "dateTime": start_datetime.isoformat("T"),
                "timeZone": cls.TIME_ZONE,
            },
            "end": {
                "dateTime": (
                    start_datetime + timedelta(minutes=event.get("duration_minutes", 60))
                ).isoformat("T"),
                "timeZone": cls.TIME_ZONE,
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "popup", "minutes": 60 * 24},
                ],
            },
        }

    def create_event(self, calendar_id: str, event: Event) -> EventsResponse:
        """
        Return the given calendar by name
        """
        event_input = self._generate_event(event)
        return (
            self.service.events()
            .insert(calendarId=calendar_id, body=dict(event_input))
            .execute()
        )
