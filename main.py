from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivy.clock import Clock

class ContentNavigationDrawer(MDBoxLayout):
    pass

class MainApp(MDApp):
    dialog = None

    def testMultipleNamedParams(self, firstName, lastName):
        return "The formatted\nusername: '{} {}'".format(firstName, lastName)
    
    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.8
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

    def on_start(self):
            Clock.schedule_once(self.on_app_started, 0)
    
    def on_app_started(self, *args):
        print("App started")

    def show_info(self, *args):
        self.root.ids['screen_manager'].current = "about"
        text = self.testMultipleNamedParams(firstName="John", lastName="Smith")
        Snackbar(text=text).open()

    def send_message(self, text):
        Snackbar(text=text).open()
    
    def more_info(self):
        title = self.root.appName
        self.dialog = MDDialog(title=title, text="This is a test dialog", auto_dismiss=True,
                buttons=[
                    MDFlatButton(text="OK", theme_text_color="Primary", on_release=lambda _: self.on_dialog_close("OK")),
                    MDFlatButton(text="Cancel", on_release=lambda _: self.on_dialog_close("Cancel")),
                ],
        )
        self.dialog.open()
    
    def toggle_theme(self):
        if self.theme_cls.theme_style == "Dark":
            self.theme_cls.theme_style = "Light"
        else:
            self.theme_cls.theme_style = "Dark"
    
    def on_dialog_close(self, action):
        self.dialog.dismiss()
        Snackbar(text=action).open()
    
    def exit(self):
        self.stop()

if __name__ == '__main__':
    MainApp().run()
