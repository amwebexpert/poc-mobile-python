import logging
from typing import Callable
from kivy.network.urlrequest import UrlRequest
import json

from libs.features.ai_chat.chat.model.chat_item import ChatItem, ChatItemRole
from libs.features.ai_chat.chat.model.chat_session import ChatSession

URL = "https://api.openai.com/v1/chat/completions"

class ChatGptService:
    messages: list[str]
    api_key: str
    model: str
    temperature: float
    ai_system_initial_context: str

    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo", ai_system_initial_context: str = "You are a helpful assistant.", temperature: float = 0.7):
        self.model = model
        self.temperature = temperature
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

    def build_new_message(self, text: str) -> dict:
        self.messages.append({"role": "user", "content": text})
        return {
            "model": self.model,
            "temperature" : self.temperature,
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

    def generate_summary_title(self, question: str, on_success: Callable) -> None:
        UrlRequest(
            URL,
            req_body = json.dumps(self.build_generate_summary_title(question)),
            req_headers = self.build_headers(),
            on_success = lambda request, response: on_success(response["choices"][0]["message"]["content"]),
            on_failure = lambda request, response: logging.error(response),
            on_error = lambda request, response: logging.error(response)
        )

    def build_generate_summary_title(self, question: str) -> None:
        messages = [{"role": "system", "content": "You are expert at summarizing long questions as small titles."}]

        content = f'Respond with a title that summarize it in its original language the following question with a maximum of 5 words.\n\nQuestion: "{question} ?"\n\nTitle:\n\n'
        messages.append({"role": "user", "content": content})

        return {
            "model": self.model,
            "temperature" : self.temperature,
            "messages" : messages,
            "n" : 1,
            "stream" : False,
            "presence_penalty" : 0,
            "frequency_penalty" : 0,
        }
