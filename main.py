from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.chip import MDChip
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.lang import Builder

class MainApp(MDApp):
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def testMultipleNamedParams(self, firstName, lastName):
        return "The formatted\nusername: '{} {}'".format(firstName, lastName)
    
    def build(self):
        self.title = "Open Mindset"
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.8
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.root = Builder.load_file("app.kv")

    def on_start(self):
            Clock.schedule_once(self.on_app_started, 0)
    
    def on_app_started(self, *args):
        print("App started")
        print(MDApp.get_running_app().root.ids.screen_manager.get_screen("settings").ids)
        print(MDApp.get_running_app().root.ids.screen_manager.get_screen("about").ids)

    def show_info(self, *args):
        self.root.ids['screen_manager'].current = "about"
        text = self.testMultipleNamedParams(firstName="John", lastName="Smith")
        Snackbar(text=text).open()

    def exit(self):
        self.stop()

if __name__ == '__main__':
    MainApp().run()
