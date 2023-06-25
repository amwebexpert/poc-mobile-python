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
from libs.utils.app_utils import get_app_screen
from libs.utils.preferences_service import PreferencesService, Preferences

from kivy.factory import Factory
from kivy.lang import Builder
import requests
import os
  
Builder.load_file('libs/features/home/home_screen.kv')

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = PreferencesService()
        Clock.schedule_once(self.init_chat_history, 0)
        #Clock.schedule_once(self.init_chat_session, 1)

    def init_chat_history(self, *args):
        screen = get_app_screen("home")
        chat_list = screen.ids['chat_list']

        chatItem = Factory.AdaptativeLabelBox()
        chatItem.ids.label.text = "Hello, here is the main chat window to interact with the AI server bot. Type in your query below and AI bot will try to answer your questions."
        card = Factory.AdaptativeVerticalCardLayout()
        card.add_widget(chatItem)
        chat_list.add_widget(card)

        chatItem = Factory.AdaptativeLabelBox()
        chatItem.ids.label.text = "Hello!"
        card = Factory.AdaptativeVerticalCardLayout()
        card.add_widget(chatItem)
        chat_list.add_widget(card)

    def init_chat_session(self, *args):
        api_key = self.service.get(Preferences.OPEN_AI_KEY.name)
        if (api_key == None):
            return

        URL = "https://api.openai.com/v1/chat/completions"
        messages = [
            {"role": "system", "content": f"You are an assistant who helps people learn."},
            {"role": "user", "content": f"Write fun fact about Albert Einstein."}
        ]
        payload = {
            "model": "gpt-3.5-turbo",
            "temperature" : 1.0,
            "top_p" : 1.0,
            "n" : 1,
            "stream" : False,
            "presence_penalty" : 0,
            "frequency_penalty" : 0,
            "messages" : messages
        }

        headers = { "Content-Type": "application/json", "Authorization": f"Bearer {api_key}" }

        response = requests.post(URL, headers=headers, json=payload)
        response = response.json()

        print(response['choices'][0]['message']['content']) 


    def send_message(self, text):
        Snackbar(text=text).open()
