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

def is_mobile():
    platform_name = platform.system().lower()
    platform_release = platform.release().lower()
    return "android" in platform_name or "ios" in platform_name or "android" in platform_release
