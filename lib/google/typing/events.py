"""
Module that configures type hints for the google services. 

This is needed as google creates the services dynamically and does not provide static typing
"""

from typing import TypedDict, Literal, Dict, Any, NotRequired, Protocol


class EventsResource(Protocol):
    def list(self, calendarId: str, **kwargs: Any) -> Any: ...
    def get(self, calendarId: str, eventId: str, **kwargs: Any) -> Any: ...
    def insert(self, calendarId: str, body: dict, **kwargs: Any) -> Any: ...
    def delete(self, calendarId: str, eventId: str, **kwargs: Any) -> Any: ...


class EventDateTime(TypedDict):
    dateTime: NotRequired[str]  # ISO format datetime
    date: NotRequired[str]  # YYYY-MM-DD format
    timeZone: NotRequired[str]


class EventAttendee(TypedDict):
    email: str
    responseStatus: Literal["needsAction", "declined", "tentative", "accepted"]
    displayName: NotRequired[str]
    organizer: NotRequired[bool]
    self: NotRequired[bool]
    resource: NotRequired[bool]
    optional: NotRequired[bool]
    comment: NotRequired[str]
    additionalGuests: NotRequired[int]


class EventReminder(TypedDict):
    method: Literal["email", "popup"]
    minutes: int


class EventReminders(TypedDict):
    useDefault: bool
    overrides: NotRequired[list[EventReminder]]


class EventCreator(TypedDict):
    email: str
    displayName: NotRequired[str]
    self: NotRequired[bool]


class EventOrganizer(TypedDict):
    email: str
    displayName: NotRequired[str]
    self: NotRequired[bool]


class ConferenceData(TypedDict):
    conferenceId: str
    conferenceSolution: Dict[str, Any]  # Could be further typed if needed
    entryPoints: list[Dict[str, Any]]  # Could be further typed if needed
    signature: NotRequired[str]


class Event(TypedDict):
    # Required fields
    id: str
    status: Literal["confirmed", "tentative", "cancelled"]
    htmlLink: str
    created: str
    updated: str
    summary: str
    creator: EventCreator
    organizer: EventOrganizer
    start: EventDateTime
    end: EventDateTime

    # Optional fields
    description: NotRequired[str]
    location: NotRequired[str]
    colorId: NotRequired[str]
    recurrence: NotRequired[list[str]]
    recurringEventId: NotRequired[str]
    originalStartTime: NotRequired[EventDateTime]
    transparency: NotRequired[Literal["opaque", "transparent"]]
    visibility: NotRequired[Literal["default", "public", "private", "confidential"]]
    iCalUID: NotRequired[str]
    sequence: NotRequired[int]
    attendees: NotRequired[list[EventAttendee]]
    reminders: NotRequired[EventReminders]
    conferenceData: NotRequired[ConferenceData]
    hangoutLink: NotRequired[str]
    anyoneCanAddSelf: NotRequired[bool]
    guestsCanInviteOthers: NotRequired[bool]
    guestsCanModify: NotRequired[bool]
    guestsCanSeeOtherGuests: NotRequired[bool]
    privateCopy: NotRequired[bool]
    locked: NotRequired[bool]
    source: NotRequired[Dict[str, str]]
    attachments: NotRequired[list[Dict[str, Any]]]


class EventsResponse(TypedDict):
    kind: Literal["calendar#events"]
    etag: str
    summary: str
    updated: str
    timeZone: str
    accessRole: str
    items: list[Event]
    nextPageToken: NotRequired[str]
    nextSyncToken: NotRequired[str]
    defaultReminders: NotRequired[list[Dict[str, Any]]]


class EventInput(TypedDict):
    summary: str
    location: NotRequired[str]
    description: NotRequired[str]
    start: EventDateTime
    end: EventDateTime
    recurrence: NotRequired[list[str]]  # RRULE, EXRULE, RDATE and EXDATE entries
    attendees: NotRequired[list[EventAttendee]]
    reminders: NotRequired[EventReminders]
    # Additional optional fields that are commonly used
    colorId: NotRequired[str]
    transparency: NotRequired[Literal["opaque", "transparent"]]
    visibility: NotRequired[Literal["default", "public", "private", "confidential"]]
    anyoneCanAddSelf: NotRequired[bool]
    guestsCanInviteOthers: NotRequired[bool]
    guestsCanModify: NotRequired[bool]
    guestsCanSeeOtherGuests: NotRequired[bool]
