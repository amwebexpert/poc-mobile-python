import json
import os
from pathlib import Path

from event_bus import EventBus

# global events bus
bus = EventBus()


def get_app_version_info() -> dict:
    return json.load(open("libs/assets/app.json", encoding="utf-8"))


def get_app_version_info_string() -> str:
    infos = get_app_version_info()
    return f"{infos['name']} v{infos['version']} ({infos['version_date']})"


def get_app_version_info_short_string() -> str:
    infos = get_app_version_info()
    return f"{infos['version']} ({infos['version_date']})"


def get_app_name() -> str:
    infos = get_app_version_info()
    return infos["name"]


def list_kv_files_to_watch() -> set:
    # including main.kv makes the app loading screens twice
    # kv_files = [os.path.join(os.getcwd(), "main.kv")]
    kv_files = []
    app_libs_dir = os.path.join(os.getcwd(), "libs")
    for path in Path(app_libs_dir).rglob('*.kv'):
        if not path.name == "theme.kv":
            kv_files.append(str(path.resolve()))
    return set(kv_files)
