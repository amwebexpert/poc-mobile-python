from kaki.app import App

from kivy.factory import Factory
from kivy.clock import Clock
from kivy.core.window import Window

from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp

from libs.utils.app_utils import get_app_version_info, get_app_version_info_string, list_kv_files_to_watch
from libs.utils.screen_utils import init_screen, is_mobile
from libs.theme.theme_utils import PRIMARY_COLORS, ThemeMode
from libs.utils.preferences_service import PreferencesService, Preferences

# https://youtube.com/watch?v=sa4AVMjjzNo
Window.keyboard_anim_args = {'d': 0.2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"

class AppScreen(MDScreen):
    pass

class MainApp(MDApp, App):
    AUTORELOADER_PATHS = [(".", {"recursive": True}) ]
    AUTORELOADER_IGNORE_PATTERNS = [ "*.pyc", "*__pycache__*", "*.db", "*.db-journal"]
    KV_FILES = list_kv_files_to_watch()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon = "libs/assets/logo.ico"
        init_screen()

    def is_mobile_device(self):
        return is_mobile()

    def get_metadata(self):
        return get_app_version_info()

    def build_app(self):
        self.service = PreferencesService()
        self.title = self.get_metadata()["name"]
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.8
        self.theme_cls.theme_style = self.service.get(Preferences.THEME_STYLE.name, default_value=ThemeMode.Dark.name)
        self.theme_cls.primary_palette = self.service.get(Preferences.THEME_PRIMARY_COLOR.name, default_value=PRIMARY_COLORS[0])

        self.screen = Factory.AppScreen()
        return self.screen

    def on_start(self):
        Clock.schedule_once(self.on_app_started, 0)
    
    def on_app_started(self, *args):
        self.screen.ids['screen_manager'].current = "home"
        info = get_app_version_info_string()
        print(f"App <{info}> started.")

    def on_stop(self):
        print("App stopped.")

    def show_info(self, *args):
        self.screen.ids['screen_manager'].current = "about"

    def exit(self):
        Clock.schedule_once(self.stop, 0)

if __name__ == '__main__':
    MainApp().run()
