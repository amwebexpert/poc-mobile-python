import platform
import os
import webbrowser

from kivy.clock import Clock
from kivy import platform as kivy_platform

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRectangleFlatIconButton

from libs.theme.base_screen import BaseScreen
from libs.utils.screen_utils import is_screen_sm
from libs.utils.app_utils import get_app_version_info_short_string, get_app_name


class AboutScreen(BaseScreen):  # pylint: disable=too-many-ancestors
    dialog = None

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.add_platform_infos, 0)

    def get_app_version_info_short_string(self) -> str:
        return get_app_version_info_short_string()

    def get_app_name(self) -> str:
        return get_app_name()

    def more_info(self) -> None:
        title = "Copyrights and licences"
        # pylint: disable-next=line-too-long
        text = """This app uses open sources libraries under common licences (MIT, Apache 2.0, etc.) and other assets registered under Creative Commons (Attribution 3.0 Unported). \n\nThe full list of licences and assets is available on the app's github page. The app's logo is original creation of Eucalyp Studio"""

        git_hub_action_text = "GitHub" if is_screen_sm() else "GitHub Project"
        logo_action_text = "Logo" if is_screen_sm() else "Eucalyp Studio"
        buttons = [
            MDRectangleFlatIconButton(text=git_hub_action_text, icon="github",
                                      on_release=lambda _: webbrowser.open("https://github.com/amwebexpert/poc-mobile-python")),
            MDRectangleFlatIconButton(text=logo_action_text, icon="link-variant",
                                      on_release=lambda _: webbrowser.open("https://www.flaticon.com/authors/eucalyp")),
        ]

        if not is_screen_sm():
            buttons.append(MDFlatButton(
                text="Close", on_release=lambda _: self.dialog.dismiss()))

        self.dialog = MDDialog(title=title, text=text,
                               auto_dismiss=True, buttons=buttons)
        self.dialog.open()

    def add_platform_infos(self, *_args) -> None:
        screen = self.manager.get_screen("about")
        infos_panel = screen.ids["infos_panel"]

        infos_panel.add_row(("Platform", kivy_platform))
        infos_panel.add_row(("Platform release", platform.release()))
        infos_panel.add_row(("Platform version", platform.version()))
        infos_panel.add_row(("Platform machine", platform.machine()))
        infos_panel.add_row(("Platform node", platform.node()))
        infos_panel.add_row(("Python version", platform.python_version()))
        infos_panel.add_row(("TMPDIR", os.environ.get("TMPDIR", "-")))
