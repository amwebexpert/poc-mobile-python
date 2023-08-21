from kivy import platform

def is_android() -> bool:
    return platform == "android"

def is_ios() -> bool:
    return platform == "ios"
