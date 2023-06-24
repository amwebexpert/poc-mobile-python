from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.chip import MDChip
from kivymd.theming import ThemeManager
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.lang import Builder
from libs.utils.app_utils import get_app_screen
from kivy.core.window import Window

# https://youtube.com/watch?v=sa4AVMjjzNo
# making app crashing on Android
#window.keyboard_anim_args = {'d': 0.2, 't': 'in_out_expo'}
#window.softinput_mode = "below_target"

class AppScreen(MDScreen):
    pass

class MainApp(MDApp):
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def testMultipleNamedParams(self, firstName, lastName):
        # equivalent to: "The formatted username: '{} {}'".format(firstName, lastName)
        return f"The formatted username: '{firstName} {lastName}'..."
    
    def build(self):
        self.title = "Open Mindset"
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.8
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"

        # this is equivalent to just returning Builder.load_file(...)
        # but being explicit here for clarity about whats going on with root widget
        Builder.load_file("main_layout.kv")
        appScreen = AppScreen()
        appScreen.theme_cls = ThemeManager()
        return appScreen

    def on_start(self):
            Clock.schedule_once(self.on_app_started, 0)
    
    def on_app_started(self, *args):
        app = MDApp.get_running_app()
        print(f"App <{app.title}> started.")

    def on_stop(self):
        app = MDApp.get_running_app()
        print(f"App <{app.title}> stopped.")

    def show_info(self, *args):
        self.root.ids['screen_manager'].current = "about"
        text = self.testMultipleNamedParams(firstName="John", lastName="Smith")
        Snackbar(text=text).open()

    def exit(self):
        self.stop()

if __name__ == '__main__':
    MainApp().run()
