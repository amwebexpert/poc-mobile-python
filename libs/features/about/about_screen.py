import platform
import os
import webbrowser

from kivy.clock import Clock

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRectangleFlatIconButton

from libs.theme.base_screen import BaseScreen
from libs.utils.platform_utils import is_android
from libs.utils.screen_utils import is_mobile
from libs.utils.app_utils import get_app_version_info_short_string, get_app_name

class AboutScreen(BaseScreen):
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
        text = """This app uses open sources libraries under common licences (MIT, Apache 2.0, etc.) and other assets registered under Creative Commons (Attribution 3.0 Unported). \n\nThe full list of licences and assets is available on the app's github page. The app's logo is original creation of Eucalyp Studio"""

        gitHubActionText = "GitHub" if is_mobile() else "GitHub Project"
        logoActionText = "Logo" if is_mobile() else "Eucalyp Studio"
        buttons = [
            MDRectangleFlatIconButton(text=gitHubActionText, icon="github",
                on_release=lambda _: webbrowser.open("https://github.com/amwebexpert/poc-mobile-python")),
            MDRectangleFlatIconButton(text=logoActionText, icon="link-variant",
                on_release=lambda _: webbrowser.open("https://www.flaticon.com/authors/eucalyp")),
        ]

        if not is_mobile():
            buttons.append(MDFlatButton(text="Close", on_release=lambda _: self.dialog.dismiss()))

        self.dialog = MDDialog(title=title, text=text, auto_dismiss=True, buttons=buttons)
        self.dialog.open()

    def add_platform_infos(self, *args) -> None:
        screen = self.manager.get_screen("about")
        infos_panel = screen.ids["infos_panel"]

        if is_android():
            infos_panel.add_row(("Platform", "Android"))
        else:
            infos_panel.add_row(("Platform", platform.system()))            
        infos_panel.add_row(("Platform release", platform.release()))
        infos_panel.add_row(("Platform version", platform.version()))
        infos_panel.add_row(("Platform machine", platform.machine()))
        infos_panel.add_row(("Platform node", platform.node()))
        infos_panel.add_row(("Python version", platform.python_version()))
        infos_panel.add_row(("TMPDIR", os.environ.get("TMPDIR", "-")))
