from kivymd.uix.widget import Widget
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import Snackbar

from kivy.lang import Builder
  
Builder.load_file('libs/features/about/about_screen.kv')

class AboutScreen(MDScreen):
    dialog = None

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
