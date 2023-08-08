import logging

from libs.theme.base_screen import BaseScreen
from libs.utils.app_utils import bus

class HomeScreen(BaseScreen):

    @bus.on("app_started_event")
    def handle_app_started_event(info: str = "") -> None:
        logging.debug(f"HomeScreen: App <{info}> started.")
