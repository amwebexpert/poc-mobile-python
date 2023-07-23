import logging

from kivy.factory import Factory
from kivy.clock import Clock
from kivy.uix.screenmanager import SlideTransition, NoTransition

from kivymd.uix.screen import MDScreen
from kivymd.tools.hotreload.app import MDApp
from kivymd.toast import toast

import pyperclip

from libs.utils.app_utils import get_app_version_info, get_app_version_info_string, list_kv_files_to_watch, bus
from libs.utils.keyboard_utils import init_keyboard
from libs.utils.screen_utils import init_screen, is_mobile
from libs.theme.theme_utils import PRIMARY_COLORS, ThemeMode
from libs.utils.preferences_service import PreferencesService, Preferences

class AppScreen(MDScreen):
    pass

class MainApp(MDApp):
    AUTORELOADER_PATHS = [(".", {"recursive": True}) ]
    AUTORELOADER_IGNORE_PATTERNS = [ "*.pyc", "*__pycache__*", "*.db", "*.db-journal"]
    KV_FILES = list_kv_files_to_watch()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        init_screen()

    def is_mobile_device(self) -> bool:
        return is_mobile()

    def get_metadata(self) -> dict:
        return get_app_version_info()

    def build_app(self):
        self.service = PreferencesService()
        self.title = self.get_metadata()["name"]
        self.icon = "libs/assets/logo.ico"
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.8
        self.theme_cls.theme_style = self.service.get(Preferences.THEME_STYLE.name, default_value=ThemeMode.Dark.name)
        self.theme_cls.primary_palette = self.service.get(Preferences.THEME_PRIMARY_COLOR.name, default_value=PRIMARY_COLORS[0])

        appScreen = Factory.AppScreen()
        self.screen_manager = appScreen.ids["screen_manager"]
        return appScreen

    def on_start(self) -> None:
        Clock.schedule_once(self.on_app_started, 0)
    
    def on_app_started(self, *args) -> None:
        self.screen_manager.transition = NoTransition()
        self.screen_manager.current = "home"
        self.screen_manager.transition = SlideTransition()
        bus.emit("app_started_event", get_app_version_info_string())

    def on_stop(self) -> None:
        logging.debug("App stopped.")

    def show_info(self, *args) -> None:
        self.screen_manager.current = "about"

    @bus.on("app_started_event")
    def handle_app_started_event(info = "") -> None:
        logging.debug(f"App <{info}> started.")

    def copy_text_to_clipboard(self, text) -> None:
        pyperclip.copy(text)
        toast(text = f'Content copied: "{text[0:20]}"...', duration = 2)

    def exit(self) -> None:
        Clock.schedule_once(self.stop, 0)

if __name__ == '__main__':
    init_keyboard()
    MainApp().run()
