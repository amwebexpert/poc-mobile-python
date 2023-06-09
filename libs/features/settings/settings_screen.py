from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.widget import Widget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.menu import MDDropdownMenu

from kivy.lang import Builder
from kivy.clock import Clock
from libs.theme.theme_utils import PRIMARY_COLORS, ThemeMode
from libs.utils.preferences_service import PreferencesService, Preferences
  
class SettingsScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = PreferencesService()
        Clock.schedule_once(self.init_ui, 0)
    
    def getUIElement(self, name):
        screen = self.manager.get_screen("settings")
        return screen.ids[name]
    
    def init_ui(self, *args):
        self.init_primary_colors_drop_down_list()
        self.init_ai_system_context()
        self.init_api_key()
        self.init_ai_temperature()

    def init_ai_system_context(self):
        value = self.service.get(Preferences.AI_SYSTEM_INITIAL_CONTEXT.name, default_value="You are a helpful assistant.")
        self.getUIElement("ai_system_initial_context").text = value

    def init_api_key(self):
        value = self.service.get(Preferences.OPEN_AI_KEY.name)
        if value is not None:
            self.getUIElement("open_ai_key").text = value

    def init_ai_temperature(self):
        value = self.service.get(Preferences.AI_TEMPERATURE.name, 0)
        self.getUIElement("ai_temperature").value = value

    def init_primary_colors_drop_down_list(self):
        menu_items = [
            {
                "text": color,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=color: self.on_color_selected(x),
            } for color in PRIMARY_COLORS
        ]
        self.menu = MDDropdownMenu(
            caller = self.getUIElement("primary_color_menu_button"),
            items = menu_items,
            width_mult = 4,
        )
        color = self.service.get(Preferences.THEME_PRIMARY_COLOR.name, default_value=PRIMARY_COLORS[0])
        self.getUIElement("primary_color_menu_button").set_item(color)

    def open_color_menu(self):
        self.menu.open()
    
    def on_color_selected(self, color):
        self.getUIElement("primary_color_menu_button").set_item(color)
        theme = MDApp.get_running_app().theme_cls
        theme.primary_palette = color
        self.service.set(Preferences.THEME_PRIMARY_COLOR.name, color)
        self.menu.dismiss()

    def toggle_theme(self):
        theme = MDApp.get_running_app().theme_cls
        theme.theme_style = ThemeMode.Dark.name if theme.theme_style == ThemeMode.Light.name else ThemeMode.Light.name
        self.service.set(Preferences.THEME_STYLE.name, theme.theme_style)

    def set_open_ai_key(self, text):
        self.service.set(Preferences.OPEN_AI_KEY.name, text)

    def set_ai_initial_context(self, text):
        self.service.set(Preferences.AI_SYSTEM_INITIAL_CONTEXT.name, text)
    
    def set_ai_temperature(self, value):
        self.service.set(Preferences.AI_TEMPERATURE.name, round(value, 2))
