"""
Module that configures type hints for the google services. 

This is needed as google creates the services dynamically and does not provide static typing
"""

from typing import Any, Literal, Optional, Protocol, TypedDict

from lib.google.typing.events import EventsResource


class CalendarListResource(Protocol):
    def list(self, **kwargs: Any) -> Any: ...
    def get(self, calendarId: str, **kwargs: Any) -> Any: ...
    def insert(self, body: dict, **kwargs: Any) -> Any: ...
    def delete(self, calendarId: str, **kwargs: Any) -> Any: ...


class CalendarService(Protocol):
    def calendarList(self) -> CalendarListResource: ...
    def events(self) -> EventsResource: ...


class NotificationMethod(TypedDict):
    method: Literal["email", "sms", "popup"]
    type: Literal[
        "eventCreation",
        "eventChange",
        "eventCancellation",
        "eventResponse",
        "agenda",
        "reminder",
    ]


class CalendarListEntryNotificationSettings(TypedDict):
    notifications: list[NotificationMethod]


class CalendarListEntryConferenceProperties(TypedDict):
    allowedConferenceSolutionTypes: list[str]


class CalendarListEntry(TypedDict):
    kind: Literal["calendar#calendarListEntry"]
    etag: str
    id: str
    summary: str
    description: Optional[str]
    location: Optional[str]
    timeZone: Optional[str]
    summaryOverride: Optional[str]
    colorId: Optional[str]
    backgroundColor: str
    foregroundColor: str
    hidden: Optional[bool]
    selected: Optional[bool]
    accessRole: Literal["none", "freeBusyReader", "reader", "writer", "owner"]
    defaultReminders: list[dict]  # You can further define reminder structure if needed
    notificationSettings: Optional[CalendarListEntryNotificationSettings]
    primary: Optional[bool]
    deleted: Optional[bool]
    conferenceProperties: Optional[CalendarListEntryConferenceProperties]


class CalendarListResponse(TypedDict):
    kind: Literal["calendar#calendarList"]
    etag: str
    nextPageToken: Optional[str]
    nextSyncToken: Optional[str]
    items: list[CalendarListEntry]
