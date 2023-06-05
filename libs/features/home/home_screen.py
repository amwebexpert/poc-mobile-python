from kivymd.app import MDApp
from kivymd.uix.widget import Widget
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import Snackbar

from kivy.lang import Builder
  
Builder.load_file('libs/features/home/home_screen.kv')

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def send_message(self, text):
        print(MDApp.get_running_app().root.ids.screen_manager.get_screen("settings").ids)
        print(MDApp.get_running_app().root.ids.screen_manager.get_screen("about").ids)
        Snackbar(text=text).open()
