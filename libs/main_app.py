import logging
import subprocess

from kaki.app import App

from kivy.factory import Factory
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard

from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.toast import toast

from libs.utils.app_utils import get_app_version_info, get_app_version_info_string, list_kv_files_to_watch, bus
from libs.utils.platform_utils import is_android
from libs.utils.screen_utils import init_screen, is_screen_sm
from libs.theme.theme_utils import PRIMARY_COLORS, ThemeMode
from libs.features.settings.preferences_service import PreferencesService, Preferences


class AppScreen(MDScreen):  # pylint: disable=too-many-ancestors
    pass


class MainApp(MDApp, App):
    AUTORELOADER_PATHS = [(".", {"recursive": True})]
    AUTORELOADER_IGNORE_PATTERNS = [
        "*.pyc", "*__pycache__*", "*.db", "*.db-journal"]
    KV_FILES = list_kv_files_to_watch()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.service = PreferencesService()
        self.screen_manager = None
        self.app_navigation_bar = None
        init_screen()

    def is_screen_sm(self) -> bool:
        return is_screen_sm()

    def get_metadata(self) -> dict:
        return get_app_version_info()

    def build_app(self) -> AppScreen:  # pylint: disable=arguments-differ
        self.title = self.get_metadata()["name"]
        self.icon = "libs/assets/logo.ico"
        self.init_theme()

        app_screen = Factory.AppScreen()
        self.init_app_navigation(app_screen)
        return app_screen

    def init_theme(self) -> None:
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.8
        self.theme_cls.theme_style = self.service.get(
            Preferences.THEME_STYLE.name, default_value=ThemeMode.Dark.name)
        self.theme_cls.primary_palette = self.service.get(
            Preferences.THEME_PRIMARY_COLOR.name, default_value=PRIMARY_COLORS[0])

    def init_app_navigation(self, app_screen: AppScreen) -> None:
        self.screen_manager = app_screen.ids['screen_manager']
        self.app_navigation_bar = app_screen.ids['app_navigation_bar']
        self.app_navigation_bar.screen_manager = self.screen_manager
        self.app_navigation_bar.navigate_to("home")

    def on_start(self) -> None:
        Clock.schedule_once(self.on_app_started, 0)

    def on_app_started(self, *_args) -> None:
        bus.emit("app_started_event", get_app_version_info_string())

    def on_stop(self) -> None:
        logging.debug("App stopped.")

    def copy_text_to_clipboard(self, text: str) -> None:
        Clipboard.copy(text)
        toast(text=f'Content copied: "{text[0:20]}"...', duration=2)

    def open_file(self, filename: str) -> None:
        if is_android():
            # TODO - either copy file to an android public or create an OPEN android Intent, or both:
            # https://stackoverflow.com/questions/3590955/intent-to-launch-the-clock-application-on-android
            # https://www.albertgao.xyz/2017/05/22/how-to-get-current-app-folder-in-kivy/
            # for now: just copy filename to the clipboard
            root_folder = self.user_data_dir
            # TODO use os.path.join instead of an f string
            fullfilename = f"{root_folder}/{filename}"
            self.copy_text_to_clipboard(text=fullfilename)
        else:
            subprocess.run(['open', filename], check=True)

    def exit(self) -> None:
        Clock.schedule_once(self.stop, 0)


@bus.on("app_started_event")
def handle_app_started_event(info="") -> None:
    logging.debug("App <%s> started.", info)
