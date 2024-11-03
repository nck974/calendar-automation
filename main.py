"""
Entrypoint of the script
"""
from datetime import datetime

from dotenv import load_dotenv

from lib.google.calendar import GoogleCalender
from lib.model.event import Event

CALENDAR_NAME = "Hochschule Konzerte"

def main():
    """
    Run program
    """
    load_dotenv()
    google_calender = GoogleCalender()

    # Find correct calendar
    calendar = google_calender.get_calender_by_name(CALENDAR_NAME)
    calendar_id = calendar["id"]

    # Create an event
    event_input = Event(
        name="Feierliche Übergabe der Rotary-Viola - (Kammermusiksaal) - Free",
        description="Concert",
        start_datetime=datetime(2024, 11, 5, 19, 30),
        duration_minutes=60,
    )
    event = google_calender.create_event(calendar_id, event_input)
    print(event)


if __name__ == "__main__":
    main()
