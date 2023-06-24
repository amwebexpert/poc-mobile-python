from kivy.metrics import dp
from kivymd.uix.widget import Widget
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import Snackbar

from libs.utils.app_utils import get_app_screen

from kivy.clock import Clock
from kivy.lang import Builder
  
Builder.load_file('libs/features/about/about_screen.kv')

class AboutScreen(MDScreen):
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.add_platform_infos, 0)

    def more_info(self):
        title = "Open Mindset"
        self.dialog = MDDialog(title=title, text="This is a test dialog", auto_dismiss=True,
                buttons=[
                    MDFlatButton(text="OK", theme_text_color="Primary", on_release=lambda _: self.on_dialog_close("OK")),
                    MDFlatButton(text="Cancel", on_release=lambda _: self.on_dialog_close("Cancel")),
                ],
        )
        self.dialog.open()

    def on_dialog_close(self, action):
        self.dialog.dismiss()
        Snackbar(text=action).open()

    def add_platform_infos(self, *args):
        screen = get_app_screen("about")
        infos_panel = screen.ids['infos_panel']
        infos_panel.add_row(("Platform", "Android"))

