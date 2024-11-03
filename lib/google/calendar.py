"""
Module to manage the calenders
"""

from datetime import timedelta
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


class GoogleCalender:
    """
    Manage API calls to the Google Calender API
    """

    # Configure the maximum pages that will be searched
    MAX_PAGES: Final[int] = int(os.environ.get(Env.MAX_SEARCH_CALENDAR_PAGES.value) or 10)
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

    def get_calenders(self) -> list[CalendarListEntry]:
        """
        Return the list of available calenders
        """
        page_token = None
        calenders: list[CalendarListEntry] = []
        for _ in range(self.MAX_PAGES):
            calender_response: CalendarListResponse = (
                self.service.calendarList().list(pageToken=page_token).execute()
            )
            if "items" in calender_response:
                calenders = calenders + calender_response["items"]

            page_token = calender_response.get("nextPageToken")
            if not page_token:
                break

        return calenders

    def get_calender_by_name(self, name: str) -> CalendarListEntry:
        """
        Return the given calender by name
        """
        calendars = self.get_calenders()
        for calendar in calendars:
            if calendar["summary"] == name.strip():
                return calendar

        raise ResourceNotFoundException

    @classmethod
    def _generate_event(cls, event: Event) -> EventInput:
        """
        Return the event input object expected by the google
        """
        return {
            "summary": event.name,
            "description": event.description,
            "start": {
                "dateTime": event.start_datetime.isoformat("T"),
                "timeZone": cls.TIME_ZONE,
            },
            "end": {
                "dateTime": (
                    event.start_datetime + timedelta(minutes=event.duration_minutes)
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
        Return the given calender by name
        """
        event_input = self._generate_event(event)
        return (
            self.service.events()
            .insert(calendarId=calendar_id, body=dict(event_input))
            .execute()
        )
