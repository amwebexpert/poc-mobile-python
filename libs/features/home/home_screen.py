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

from kivy.factory import Factory
from kivy.lang import Builder
  
Builder.load_file('libs/features/home/home_screen.kv')

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.init_chat_history, 1)

    def init_chat_history(self, *args):
        screen = get_app_screen("home")
        chat_list = screen.ids['chat_list']

        chatItem = Factory.AdaptativeLabelBox()
        chatItem.ids.label.text = "Hello, here is the main chat window to interact with the AI server bot. Type in your query below and AI bot will try to answer your questions."
        card = Factory.AdaptativeVerticalCardLayout()
        card.size_hint_x: 0.5
        card.add_widget(chatItem)
        chat_list.add_widget(card)

        chatItem = Factory.AdaptativeLabelBox()
        chatItem.ids.label.text = "Hello!"
        card = Factory.AdaptativeVerticalCardLayout()
        card.add_widget(chatItem)
        chat_list.add_widget(card)

    def send_message(self, text):
        Snackbar(text=text).open()
