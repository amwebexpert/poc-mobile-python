from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.widget import Widget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from kivy.lang import Builder
  
Builder.load_file('libs/features/settings/settings_screen.kv')

class SettingsScreen(MDScreen):

    def toggle_theme(self):
        theme = MDApp.get_running_app().theme_cls
        if theme.theme_style == "Dark":
            theme.theme_style = "Light"
        else:
            theme.theme_style = "Dark"
