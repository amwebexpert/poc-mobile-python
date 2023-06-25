from enum import Enum
import sqlite3
from libs.utils.storage_service import StorageService

Preferences = Enum('Preferences', ['OPEN_AI_KEY', 'THEME_PRIMARY_COLOR', 'THEME_STYLE'])

class PreferencesService:
    def __init__(self):
        self.storage_service = StorageService("preferences.db")
        self.storage_service.connect()
        self.storage_service.create_table("preferences", "key TEXT, value TEXT")
        self.storage_service.close()

    def get(self, key, default_value = None):
        self.storage_service.connect()
        result = self.storage_service.select("preferences", "value", f'key = "{key}"')
        self.storage_service.close()
        if len(result) == 0:
            return default_value
        else:
            return result[0][0]

    def set(self, key, value):
        self.storage_service.connect()
        self.storage_service.insert("preferences", "key, value", f'"{key}", "{value}"')
        self.storage_service.close()

    def delete(self, key):
        self.storage_service.connect()
        self.storage_service.delete("preferences", f'key = "{key}"')
        self.storage_service.close()
