from kivy.network.urlrequest import UrlRequest
import json

URL = "https://api.openai.com/v1/chat/completions"

class ChatGptService:
    def __init__(self, api_key = None, model="gpt-3.5-turbo", ai_system_initial_context="You are a helpful assistant.", temperature=0.7, max_tokens=150):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.ai_system_initial_context = ai_system_initial_context
        self.headers = { "Content-Type": "application/json", "Authorization": f"Bearer {api_key}" }

        self.start_new_session()

    def start_new_session(self):
        self.messages = [{"role": "system", "content": self.ai_system_initial_context}]

    def build_new_message(self, text):
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

    def send_message(self, text, on_success, on_error):
        self.on_success = on_success
        self.on_error = on_error

        payload = self.build_new_message(text)
        request = UrlRequest(
            URL,
            req_body = json.dumps(payload),
            req_headers = self.headers,
            on_success = self.on_api_success,
            on_failure = self.on_api_error,
            on_error = self.on_api_error
        )

    def on_api_success(self, request, response):
        responseMessage = response["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": responseMessage})
        self.on_success(responseMessage)

    def on_api_error(self, request, response):
        print(response)
        self.on_error("Sorry, I didn't understand that.")
