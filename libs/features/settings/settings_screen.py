from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu

from kivy.clock import Clock

from libs.theme.base_screen import BaseScreen
from libs.theme.theme import PRIMARY_COLORS, ThemeMode
from libs.features.settings.preferences_service import PreferencesService, Preferences
from kivy.properties import StringProperty
from kivy import platform

class SettingsScreen(BaseScreen):  # pylint: disable=too-many-ancestors
    text_input_hint_text_open_ai = StringProperty()
    text_input_hint_text_stabilty_ai = StringProperty()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.service = PreferencesService()
        self.menu = None
        Clock.schedule_once(self.init_ui, 0)

    def init_ui(self, *_args) -> None:
        self.init_primary_colors_drop_down_list()
        self.init_ai_system_context()
        self.init_open_ai_key()
        self.init_stability_ai_key()
        self.init_ai_temperature()
        self.text_input_hint_text_open_ai = "Open AI key value (see https://platform.openai.com)"
        self.text_input_hint_text_stabilty_ai = "Stability AI key value (see https://stability.ai/)"
        self.set_text_hints()

    def init_ai_system_context(self) -> None:
        value = self.service.get(
            Preferences.AI_SYSTEM_INITIAL_CONTEXT.name, default_value="You are a helpful assistant.")
        self.get_gui_element("ai_system_initial_context").text = value

    def init_open_ai_key(self) -> None:
        value = self.service.get(Preferences.OPEN_AI_KEY.name)
        if value is not None:
            self.get_gui_element("open_ai_key").text = value

    def init_stability_ai_key(self) -> None:
        value = self.service.get(Preferences.STABILITY_AI_KEY.name)
        if value is not None:
            self.get_gui_element("stability_ai_key").text = value

    def init_ai_temperature(self) -> None:
        value = self.service.get(Preferences.AI_TEMPERATURE.name, 0)
        self.get_gui_element("ai_temperature").value = value

    def init_primary_colors_drop_down_list(self) -> None:
        menu_items = [
            {
                "text": color,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=color: self.on_color_selected(x),
            } for color in PRIMARY_COLORS
        ]
        self.menu = MDDropdownMenu(
            caller=self.get_gui_element("primary_color_menu_button"),
            items=menu_items,
            width_mult=4,
        )
        color = self.service.get(
            Preferences.THEME_PRIMARY_COLOR.name, default_value=PRIMARY_COLORS[0])
        self.get_gui_element("primary_color_menu_button").set_item(color)

    def open_color_menu(self) -> None:
        self.menu.open()

    def on_color_selected(self, color: str) -> None:
        self.get_gui_element("primary_color_menu_button").set_item(color)
        theme = MDApp.get_running_app().theme_cls
        theme.primary_palette = color
        self.service.set(Preferences.THEME_PRIMARY_COLOR.name, color)
        self.menu.dismiss()

    def toggle_theme(self) -> None:
        theme = MDApp.get_running_app().theme_cls
        theme.theme_style = ThemeMode.Dark.name if theme.theme_style == ThemeMode.Light.name else ThemeMode.Light.name
        self.service.set(Preferences.THEME_STYLE.name, theme.theme_style)

    def set_open_ai_key(self, text: str) -> None:
        self.service.set(Preferences.OPEN_AI_KEY.name, text)

    def set_stability_ai_key(self, text: str) -> None:
        self.service.set(Preferences.STABILITY_AI_KEY.name, text)

    def set_ai_initial_context(self, text: str) -> None:
        self.service.set(Preferences.AI_SYSTEM_INITIAL_CONTEXT.name, text)

    def set_ai_temperature(self, value: int) -> None:
        self.service.set(Preferences.AI_TEMPERATURE.name, round(value, 2))

    # costa-rica: the text is too long on the iPhone if we add the paste button this method will reduce the text_hint length.
    def set_text_hints(self):
        if platform == 'ios':
            self.text_input_hint_text_open_ai = "[Your Open AI key]"
            self.text_input_hint_text_stabilty_ai = "[Your Stability AI key]"