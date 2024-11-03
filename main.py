"""
Entrypoint of the script
"""


from dotenv import load_dotenv

from lib.exceptions.invalid_prompt import InvalidPromptOutputException
from lib.google.calendar import GoogleCalendar
from lib.google.gemini import Gemini
from lib.model.event import Event
from lib.prompt.event import build_find_events_prompt

CALENDAR_NAME = "CALENDAR NAME"
EVENTS_INPUT = """
ADD HERE User INPUT
"""


def get_calendar_events_with_ai() -> list[Event]:
    """
    Find the events from the given text
    """
    ai_generator = Gemini()
    events = ai_generator.send_prompt(
        build_find_events_prompt(EVENTS_INPUT),
        response_schema=list[Event],
    )

    if not isinstance(events, list) or len(events) == 0:
        raise InvalidPromptOutputException

    return list(map(lambda x: Event(x), events))


def main():
    """
    Run program
    """
    load_dotenv()
    google_calendar = GoogleCalendar()

    # Find correct calendar
    calendar = google_calendar.get_calendar_by_name(CALENDAR_NAME)
    calendar_id = calendar["id"]

    # Create al events found in the provided text
    for event in get_calendar_events_with_ai():
        event = google_calendar.create_event(calendar_id, event)
        print(f"Event created: {event['summary']}")


if __name__ == "__main__":
    main()
