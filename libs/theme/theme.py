from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior


class ImageButton(ButtonBehavior, Image):
    def on_press(self):
        pass
