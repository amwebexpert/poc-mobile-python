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
from libs.utils.chat_gpt_service import ChatGptService

from kivy.factory import Factory
from kivy.lang import Builder
from datetime import datetime
import json
  
Builder.load_file("libs/features/home/home_screen.kv")

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.preferences_service = PreferencesService()
        self.chat_gpt_service = ChatGptService(
            api_key = self.preferences_service.get(Preferences.OPEN_AI_KEY.name),
            ai_system_initial_context = self.preferences_service.get(Preferences.AI_SYSTEM_INITIAL_CONTEXT.name),
            temperature = float(self.preferences_service.get(Preferences.AI_TEMPERATURE.name))
        )
        Clock.schedule_once(self.init_chat_history, 0)

    def getUIElement(self, name):
        return get_app_screen("home").ids[name]

    def init_chat_history(self, *args):
        item = self.buildChatItemLeft("I'm an artificial intelligence helpful assistant. How can I help you?")
        self.getUIElement("chat_list").add_widget(item)

    def buildChatItemRight(self, text):
        return self.buildChatItem(chatItem=Factory.AdaptativeLabelBoxRight(), text=text, role="user")
    
    def buildChatItemLeft(self, text):
        return self.buildChatItem(chatItem=Factory.AdaptativeLabelBoxLeft(), text=text, role="assistant")

    def buildChatItem(self, chatItem, text, role):
        chatItem.ids.label.text = text
        chatItem.ids.created_at.icon = "human-greeting-variant" if role == "user" else "robot-outline"
        chatItem.ids.created_at.text = datetime.now().strftime("%m-%d-%Y %H:%M")
        return chatItem

    def send_message(self, text):
        api_key = self.preferences_service.get(Preferences.OPEN_AI_KEY.name)
        if (api_key == None):
            self.getUIElement("chat_list").add_widget(self.buildChatItemLeft("Missing OpenAI API key. Please set it in the settings screen."))
            return
        self.chat_gpt_service.send_message(text, on_success=self.on_success, on_error=self.on_error)
        self.getUIElement("chat_list").add_widget(self.buildChatItemRight(text))

    def on_success(self, responseMessage):
        self.getUIElement("chat_list").add_widget(self.buildChatItemLeft(responseMessage))

    def on_error(self, errorMessage):
        self.getUIElement("chat_list").add_widget(self.buildChatItemLeft("Sorry, I didn't understand that."))
