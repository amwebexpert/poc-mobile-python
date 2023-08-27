from typing import List
from enum import Enum

from kivy.clock import Clock
from kivy.animation import Animation
from kivy.factory import Factory

from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

from kivymd.uix.widget import Widget

PRIMARY_COLORS: List[str] = ["Red", "Pink", "Purple", "DeepPurple", "Indigo", "Blue",
                             "LightBlue", "Cyan", "Teal", "Green", "LightGreen", "Lime", "Yellow",
                             "Amber", "Orange", "DeepOrange", "Brown", "Gray", "BlueGray"]

ThemeMode: Enum = Enum("ThemeMode", ["Light", "Dark"])

ICONS = ["robot-outline", "robot-confused-outline", "robot-confused"]


class ImageButton(ButtonBehavior, Image):
    def on_press(self):
        pass

class AnimatedIcons:
    animation: Animation
    widget: Widget

    def __init__(self) -> None:
        self.widget = Factory.AnimatedRobotIcons()

        for icon in ICONS:
            self.widget.add_widget(Factory.AminatedRobotIcon(icon=icon))

        self.animation = Animation(opacity=0, d=0.7) + Animation(opacity=1, d=0.7)
        self.animation.repeat = True

    def start_animation(self):
        for index, item in enumerate(self.widget.children):
            self.start_animation_with_delay(item, index)

    def start_animation_with_delay(self, item: Widget, index: int):
        Clock.schedule_once(
            lambda _: self.animation.start(item), round(0.5 * index, 1))

    def stop_animation(self):
        for item in self.widget.children:
            self.animation.stop(item)
