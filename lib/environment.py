from enum import Enum


class Env(Enum):
    """
    Support class to configure the available environment variables
    """

    GOOGLE_API_KEY = "GOOGLE_API_KEY"
    TIME_ZONE = "TIME_ZONE"
    MAX_SEARCH_CALENDAR_PAGES = "MAX_SEARCH_CALENDAR_PAGES"
