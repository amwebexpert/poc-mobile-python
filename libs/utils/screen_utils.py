from kivy.core.window import Window
from kivy.utils import platform

def init_screen():
    if is_mobile:
        Window.maximize()
    else:
        Window.size = (620, 1024)

def get_screen_size():
    return Window.size

def get_screen_width():
    return Window.width

def get_screen_height():
    return Window.height

def is_mobile():
    return platform == 'android' | platform == 'ios' | "android" in platform.release().lower()
