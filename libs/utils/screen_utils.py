from kivy.core.window import Window
import platform

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

def is_android():
    platform_name = platform.system().lower()
    platform_release = platform.release().lower()
    return "android" in platform_name or "android" in platform_release

def is_ios():
    return "ios" in platform.system().lower()

def is_mobile():
    value = is_android() or is_ios()
    return value # To ease testing is_mobile() True on desktop, just return: not value
