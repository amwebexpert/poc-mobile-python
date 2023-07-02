from kivymd.app import MDApp
from kivymd.uix.widget import Widget
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import Snackbar
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.chip import MDChip
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from libs.utils.app_utils import get_app_screen
from libs.utils.preferences_service import PreferencesService, Preferences

from kivy.factory import Factory
from kivy.lang import Builder
from datetime import datetime
import requests
import os
import json
from functools import partial
  
Builder.load_file("libs/features/home/home_screen.kv")

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.service = PreferencesService()
        ai_system_initial_context = self.service.get(Preferences.AI_SYSTEM_INITIAL_CONTEXT.name, default_value="You are a helpful assistant.")
        self.messages = [{"role": "system", "content": ai_system_initial_context},]

        Clock.schedule_once(self.init_chat_history, 0)

    def getUIElement(self, name):
        return get_app_screen("home").ids[name]

    def init_chat_history(self, *args):
        item = self.buildChatItemLeft("I'm an artificial intelligence helpful assistant. How can I help you?")
        self.getUIElement("chat_list").add_widget(item)

    def buildChatItemRight(self, text):
        chatItem = Factory.AdaptativeLabelBoxRight()
        chatItem.ids.created_at.icon = "human-greeting-variant"
        chatItem.ids.label.text = text
        chatItem.ids.created_at.text = datetime.now().strftime("%m-%d-%Y %H:%M")
        return chatItem
    
    def buildChatItemLeft(self, text):
        chatItem = Factory.AdaptativeLabelBoxLeft()
        chatItem.ids.created_at.icon = "robot-outline"
        chatItem.ids.label.text = text
        chatItem.ids.created_at.text = datetime.now().strftime("%m-%d-%Y %H:%M")
        return chatItem

    def send_message(self, text):
        URL = "https://api.openai.com/v1/chat/completions"
        api_key = self.service.get(Preferences.OPEN_AI_KEY.name)
        if (api_key == None):
            self.getUIElement("chat_list").add_widget(self.buildChatItemLeft("Missing OpenAI API key. Please set it in the settings screen."))
            return
        self.messages.append({"role": "user", "content": text})
        payload = {
            "model": "gpt-3.5-turbo",
            "temperature" : 0.7,
            "n" : 1,
            "stream" : False,
            "presence_penalty" : 0,
            "frequency_penalty" : 0,
            "messages" : self.messages
        }

        headers = { "Content-Type": "application/json", "Authorization": f"Bearer {api_key}" }
        request = UrlRequest(URL, req_body=json.dumps(payload), req_headers=headers, on_success=self.on_success, on_failure=self.on_error, on_error=self.on_error)
        self.getUIElement("chat_list").add_widget(self.buildChatItemRight(text))

    def on_success(self, request, response):
        responseMessage = response["choices"][0]["message"]["content"]
        self.messages.append({"role": "system", "content": responseMessage})
        self.getUIElement("chat_list").add_widget(self.buildChatItemLeft(responseMessage))

    def on_error(self, request, response):
        print(response)
        self.getUIElement("chat_list").add_widget(self.buildChatItemLeft("Sorry, I didn't understand that."))
