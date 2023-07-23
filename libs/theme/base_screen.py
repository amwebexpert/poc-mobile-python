import logging

from kivymd.uix.screen import MDScreen
from kivy.uix.widget import Widget

from libs.utils.screen_utils import get_screen

class BaseScreen(MDScreen):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def getUIElement(self, name: str) -> Widget:
        screen = get_screen(self.name)
        return screen.ids[name]

    def on_enter(self, *args) -> None:
        logging.debug(f'Entering screen "{self.name}"')
