import logging
from typing import Callable
from kivy.network.urlrequest import UrlRequest
import json

from libs.utils.chat.model.chat_item import ChatItem, ChatItemRole
from libs.utils.chat.model.chat_session import ChatSession

URL = "https://api.openai.com/v1/chat/completions"

class ChatGptService:
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo", ai_system_initial_context: str = "You are a helpful assistant.", temperature: float = 0.7, max_tokens: int = 150):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.ai_system_initial_context = ai_system_initial_context

        self.set_api_key(api_key)
        self.start_new_session()

    def set_api_key(self, api_key: str) -> None:
        self.api_key = api_key

    def start_new_session(self) -> None:
        self.messages = [{"role": "system", "content": self.ai_system_initial_context}]

    def resume_existing_session(self, chat_session: ChatSession) -> None:
        self.start_new_session()
        for chat_item in chat_session.items:
            self.add_from_chat_item(chat_item)

    def add_from_chat_item(self, chat_item: ChatItem) -> None:    
        role = "user" if int(chat_item.role) == ChatItemRole.me.value else "assistant"
        self.messages.append({"role": role, "content": chat_item.description})

    def build_new_message(self, text: str) -> None:
        self.messages.append({"role": "user", "content": text})
        return {
            "model": self.model,
            "temperature" : self.temperature,
            "max_tokens" : self.max_tokens,
            "messages" : self.messages,
            "n" : 1,
            "stream" : False,
            "presence_penalty" : 0,
            "frequency_penalty" : 0,
        }

    def build_headers(self) -> dict:
        return { "Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}" }

    def send_message(self, text: str, on_success: Callable, on_error: Callable) -> None:
        self.on_success = on_success
        self.on_error = on_error

        payload = self.build_new_message(text)
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
        response_message = response["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": response_message})
        self.on_success(response_message)

    def on_api_error(self, request, response: dict) -> None:
        logging.error(response)
        error_message = response["error"]["message"]
        self.on_error(error_message)
