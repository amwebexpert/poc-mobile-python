import platform

def is_android() -> bool:
    platform_name = platform.system().lower()
    platform_release = platform.release().lower()
    return "android" in platform_name or "android" in platform_release

def is_ios() -> bool:
    return "ios" in platform.system().lower()
