from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.chip import MDChip
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.app import MDApp
from kivy.clock import Clock

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
        print(MDApp.get_running_app().root.ids.screen_manager.get_screen("settings").ids)
        print(MDApp.get_running_app().root.ids.screen_manager.get_screen("about").ids)
        container = self.root.ids['chat_list']

        itemLayout = AnchorLayout(anchor_x='left')
        itemLayout.add_widget(MDChip(text="Hello, here is the main chat window to interact with the AI server bot.\nType in your query below and AI bot will try to answer your questions."))
        container.add_widget(itemLayout)

        itemLayout2 = AnchorLayout(anchor_x='right')
        itemLayout2.add_widget(MDChip(text="Hello"))
        container.add_widget(itemLayout2)

    def show_info(self, *args):
        self.root.ids['screen_manager'].current = "about"
        text = self.testMultipleNamedParams(firstName="John", lastName="Smith")
        Snackbar(text=text).open()

    def send_message(self, text):
        Snackbar(text=text).open()
    
    def exit(self):
        self.stop()

if __name__ == '__main__':
    MainApp().run()
