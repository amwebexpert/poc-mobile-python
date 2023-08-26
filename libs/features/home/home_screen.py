import logging

from libs.theme.base_screen import BaseScreen
from libs.utils.app_utils import bus


class HomeScreen(BaseScreen):  # pylint: disable=too-many-ancestors
    pass


@bus.on("app_started_event")
def handle_app_started_event(info: str = "") -> None:
    logging.debug("HomeScreen: App <%s> started.", info)
