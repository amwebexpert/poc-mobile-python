from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp

class ContentNavigationDrawer(MDBoxLayout):
    pass

class MainApp(MDApp):
    def testMultipleNamedParams(self, firstName, lastName):
        # text = self.testMultipleNamedParams(firstName="John", lastName="Smith")
        return "The formatted\nusername: '{} {}'".format(firstName, lastName)

if __name__ == '__main__':
    MainApp().run()
