from kivymd.app import MDApp
import json

def get_app_screen(screen_name):
    app = MDApp.get_running_app()
    screen_manager = app.root.ids.screen_manager
    return screen_manager.get_screen(screen_name)

def get_app_version_info():
    return json.load(open("libs/assets/app.json"))

def get_app_version_info_string():
    infos = get_app_version_info()
    return f"{infos['name']} v{infos['version']} ({infos['version_date']})"

def get_app_version_info_short_string():
    infos = get_app_version_info()
    return f"{infos['version']} ({infos['version_date']})"

def get_app_name():
    infos = get_app_version_info()
    return infos["name"]
