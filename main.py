from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp

class ContentNavigationDrawer(MDBoxLayout):
    pass

class MainApp(MDApp):
    def testMultipleNamedParams(self, firstName, lastName):
        return "The formatted\nusername: '{} {}'".format(firstName, lastName)
    
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

    def show_info(self):
        self.root.ids['screen_manager'].current = "about"
        text = self.testMultipleNamedParams(firstName="John", lastName="Smith")
        Snackbar(text=text).open()
    
    def exit(self):
        self.stop()

if __name__ == '__main__':
    MainApp().run()
