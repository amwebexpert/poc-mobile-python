import json
import os
from pathlib import Path

from event_bus import EventBus

from kivymd.app import MDApp

# global events bus
bus = EventBus()

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

def list_kv_files_to_watch():
    kv_files = [os.path.join(os.getcwd(), "main.kv")]
    appLibsDir = os.path.join(os.getcwd(), "libs")
    for path in Path(appLibsDir).rglob('*.kv'):
        if not (path.name == "theme.kv"):
            kv_files.append(str(path.resolve()))
    return set(kv_files)
