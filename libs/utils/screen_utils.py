from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window

from libs.utils.platform_utils import is_ios, is_android

def init_screen() -> None:
    if is_mobile():
        Window.maximize()
    else:
        Window.size = (800, 600)

def get_screen_size() -> tuple:
    return Window.size

def get_screen_width() -> int:
    return Window.width

def get_screen_height() -> int:
    return Window.height

def is_mobile() -> bool:
    value = is_android() or is_ios()
    return value # To ease testing is_mobile() True on desktop, just return: not value

def get_screen_manager() -> MDScreenManager:
    return MDApp.get_running_app().screen_manager

def get_screen(screen_name: str) -> MDScreen:
    return get_screen_manager().get_screen(screen_name)
