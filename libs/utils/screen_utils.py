import os
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window

from libs.utils.platform_utils import is_ios, is_android

def init_screen() -> None:
    if is_mobile_simulation():
        Window.top = 0
        Window.left = 0
        Window.size = (420, 780)
        return

    if is_screen_sm():
        Window.maximize()
    else:
        Window.size = (800, 600)

def get_screen_size() -> tuple:
    return Window.size

def get_screen_width() -> int:
    return Window.width

def get_screen_height() -> int:
    return Window.height

# https://getbootstrap.com/docs/5.0/layout/breakpoints/
def is_screen_sm() -> bool:
    return is_mobile_simulation() or get_screen_width() <= 576

def is_mobile_simulation() -> bool:
    return "MOBILE_SIMULATION" in os.environ

def get_screen_manager() -> MDScreenManager:
    return MDApp.get_running_app().screen_manager

def get_screen(screen_name: str) -> MDScreen:
    return get_screen_manager().get_screen(screen_name)
