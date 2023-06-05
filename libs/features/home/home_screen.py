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

from kivy.lang import Builder
  
Builder.load_file('libs/features/home/home_screen.kv')

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.init_chat_history, 1)

    def init_chat_history(self, *args):
        homeScreen = MDApp.get_running_app().root.ids.screen_manager.get_screen("home")
        container = homeScreen.ids['chat_list']

        itemLayout = AnchorLayout(anchor_x='left')
        itemLayout.add_widget(MDChip(text="Hello, here is the main chat window to interact with the AI server bot.\nType in your query below and AI bot will try to answer your questions."))
        container.add_widget(itemLayout)

        itemLayout2 = AnchorLayout(anchor_x='right')
        itemLayout2.add_widget(MDChip(text="Hello"))
        container.add_widget(itemLayout2)

    def send_message(self, text):
        print(MDApp.get_running_app().root.ids.screen_manager.get_screen("settings").ids)
        print(MDApp.get_running_app().root.ids.screen_manager.get_screen("about").ids)
        Snackbar(text=text).open()
