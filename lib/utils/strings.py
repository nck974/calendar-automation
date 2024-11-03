import json
import re
from typing_extensions import deprecated


@deprecated("This methods should not be needed if using gemini JSON")
def sanitize_json_response(response_text):
    """
    Extracts and sanitizes JSON data from a chatbot response.
    """
    json_pattern = r"(\{[^{}]*\}|\[[^\[\]]*\])"
    match = re.search(json_pattern, response_text, re.DOTALL)

    if match:
        json_string = match.group(0)
        try:
            return json.loads(json_string)
        except json.JSONDecodeError:
            raise ValueError("Extracted data is not valid JSON.")
    else:
        raise ValueError("No JSON data found in the response.")


@deprecated("This methods should not be needed if using gemini JSON")
def sanitize_json_list_response(response_text):
    """
    Extracts and sanitizes multiple JSON objects or arrays from a chatbot response.
    """
    json_pattern = r"(\[\s*\{.*?\}\s*\]|\{\s*\[.*?\]\s*\})"
    match = re.search(json_pattern, response_text, re.DOTALL)

    if match:
        json_string = match.group(0)
        try:
            # Attempt to parse the entire JSON structure
            json_data = json.loads(json_string)
            # Check if the parsed data is a list of JSON objects
            if isinstance(json_data, list) and all(
                isinstance(item, dict) for item in json_data
            ):
                return json_data
            else:
                raise ValueError("Extracted data is not a list of JSON objects.")
        except json.JSONDecodeError:
            raise ValueError("Extracted data is not valid JSON.")
    else:
        raise ValueError("No JSON array found in the response.")


def _test():
    """
    Verify this library
    """
    texts = [
        """{"a": "b"}""",
        """  {"a": "b"}   """,
        """  {"a": "b"}   asdas""",
        """adasds  {"a": "b"}asasdas   """,
        """{"a": "b", "c": ["a"]}""",
    ]
    for index, text in enumerate(texts, start=1):
        assert isinstance(sanitize_json_response(text), dict)
        print(f"PASS: Test json {index}")

    texts = [
        """[{"a": "b"}]""",
        """  [  {"a": "b"}]   """,
        """  [{"a": "b"}]   asdas""",
        """adasds  [{"a": "b"}]asasdas   """,
        """[{"a": "b", "c": ["a"]}]""",
    ]
    for index, text in enumerate(texts, start=1):
        assert isinstance(sanitize_json_list_response(text), list)
        print(f"PASS: Test json list {index}")


if __name__ == "__main__":
    _test()
