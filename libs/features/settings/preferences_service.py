from enum import Enum
import logging

from libs.services.storage_service import StorageService

Preferences = Enum("Preferences", ["OPEN_AI_KEY", "AI_SYSTEM_INITIAL_CONTEXT", "AI_TEMPERATURE", "THEME_PRIMARY_COLOR", "THEME_STYLE"])

class PreferencesService:
    def __init__(self) -> None:
        self.storage_service = StorageService("preferences.db")
        self.storage_service.connect()
        self.storage_service.create_table("preferences", ("key TEXT", "value TEXT"))
        self.storage_service.close()

    def get(self, key: str, default_value = None) -> str:
        try:
            self.storage_service.connect()
            result = self.storage_service.select("preferences", ["value"], f'key = "{key}"')
            self.storage_service.close()
            if len(result) == 0:
                return default_value
            else:
                return result[0][0]
        except Exception as e:
            logging.exception(f"Unexpected error: {e}")
            return default_value

    def set(self, key: str, value = None) -> None:
        self.storage_service.connect()
        self.storage_service.delete("preferences", f'key = "{key}"')
        if value is not None:
            self.storage_service.insert("preferences", ("key", "value"), (key, value))
        self.storage_service.close()

    def delete(self, key: str) -> None:
        self.storage_service.connect()
        self.storage_service.delete("preferences", f'key = "{key}"')
        self.storage_service.close()
