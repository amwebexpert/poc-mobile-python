from kivy.core.window import Window
from libs.utils.platform_utils import is_ios, is_android

def init_screen():
    if is_mobile():
        Window.maximize()
    else:
        Window.size = (800, 600)

def get_screen_size():
    return Window.size

def get_screen_width():
    return Window.width

def get_screen_height():
    return Window.height

def is_mobile():
    value = is_android() or is_ios()
    return value # To ease testing is_mobile() True on desktop, just return: not value
