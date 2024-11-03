"""
Module to make use of Gemini AI
"""

import json
import os
from typing import Any, Optional

import google.generativeai as genai
from google.generativeai import GenerativeModel
from loguru import logger

from lib.ai_provider import AiProvider


class Gemini(AiProvider):
    """
    Implementation of the AiProvider using Gemini
    """

    model: GenerativeModel

    def __init__(self) -> None:
        self._create_ai_model()

    def _create_ai_model(self):
        """
        Return the model that will be able to communicate with the AI
        """
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def send_prompt(self, prompt: str, response_schema: Optional[type]) -> Any:
        """
        Send a given prompt
        """
        response = self.model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json", response_schema=response_schema
            ),
        )
        logger.debug(type(response))
        logger.debug(response)
        logger.debug(response.text)

        return json.loads(response.text)
