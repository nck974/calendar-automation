from typing import Any, Protocol


class AiProvider(Protocol):
    """
    Interface of an AI Provider
    """

    def send_prompt(self, prompt: str, **kwargs) -> Any: ...
