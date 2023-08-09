import logging
from typing import Callable
from kivy.network.urlrequest import UrlRequest
import json

from libs.features.ai_chat.chat.model.chat_item import ChatItem, ChatItemRole
from libs.features.ai_chat.chat.model.chat_session import ChatSession

URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-beta-v2-2-2/text-to-image"

class ImageCreatorService:
    api_key: str = None
    query: str = None

    def set_api_key(self, api_key: str) -> None:
        self.api_key = api_key

    def build_payload(self, query: str) -> dict:
        return {
            "width": 512,
            "height": 512,
            "text_prompts": [{ "text": query, "weight": 1 }],
        }

    def build_headers(self) -> dict:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def send_message(self, query: str, on_success: Callable, on_error: Callable) -> None:
        self.on_success = on_success
        self.on_error = on_error

        payload = self.build_payload(query)
        headers = self.build_headers()

        request = UrlRequest(
            URL,
            req_body = json.dumps(payload),
            req_headers = headers,
            on_success = self.on_api_success,
            on_failure = self.on_api_error,
            on_error = self.on_api_error
        )

    def on_api_success(self, request, response: dict) -> None:
        base64: str = response["artifacts"][0]["base64"]
        self.on_success(base64)

    def on_api_error(self, request, response: dict) -> None:
        logging.error(response)
        error_message =  json.dumps(response)
        self.on_error(error_message)
