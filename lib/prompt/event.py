def build_find_events_prompt(text: str) -> str:
    """
    Generate a prompt to find the events in the given content
    """
    delimiter = """*******"""
    return f"""\
You are a bot assistant in charge of generating calendar events from the information provided by the user.
The text of the user will be delimited by '{delimiter}'.

You are in charge of finding the following information:
1. name: string This shall be the name of the event with the location in parenthesis, and if it is free of charge or not.
2. description: string A short description of what the event is about.
3. start_datetime: str When exactly is the event in ISO format.
4. duration_minutes: integer How long the event lasts in minutes. If the information can not be found write 60.

Example:
{{
    "name": "Feierliche Übergabe der Rotary-Viola - (Kammermusiksaal) - Free",
    "description: "Übergabe der Rotary-Viola mit Bogen und Stipendium durch den Rotary Club Nürnberg. Es musizieren ehemalige und aktuelle Stipendiatinnen und Stipendiaten."}},
    "start_datetime": "2024-11-05T19:30:00",
    "duration_minutes": 60
}}

{delimiter}{text}{delimiter}


Make sure you only return the JSON response without explanations\
"""
