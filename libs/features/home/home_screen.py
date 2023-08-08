import logging

from libs.theme.base_screen import BaseScreen
from libs.utils.app_utils import bus
from libs.utils.screen_utils import get_navigation_bar

class HomeScreen(BaseScreen):

    def ai_chat(self) -> None:
        get_navigation_bar().navigate_to("ai_chat")
    
    @bus.on("app_started_event")
    def handle_app_started_event(info: str = "") -> None:
        logging.debug(f"HomeScreen: App <{info}> started.")
