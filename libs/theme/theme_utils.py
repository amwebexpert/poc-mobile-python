from typing import List
from enum import Enum

from kivy.clock import Clock
from kivy.animation import Animation
from kivy.factory import Factory

PRIMARY_COLORS: List[str] = ["Red" , "Pink" , "Purple" , "DeepPurple" , "Indigo" , "Blue" ,
    "LightBlue" , "Cyan" , "Teal" , "Green" , "LightGreen" , "Lime" , "Yellow" ,
    "Amber" , "Orange" , "DeepOrange" , "Brown" , "Gray" , "BlueGray"]

ThemeMode: Enum = Enum("ThemeMode", ["Light", "Dark"])

class AnimatedIcons:
    icons = []

    def __init__(self, **kwargs) -> None:
        self.widget = Factory.AnimatedIconButton()

        ids = self.widget.ids
        self.icons.append(ids.animated_icon)
        self.icons.append(ids.animated_icon_2)
        self.icons.append(ids.animated_icon_3)

        self.animation = Animation(opacity=0, d=0.7) + Animation(opacity=1, d=0.7)
        self.animation.repeat = True

    def start_animation(self):
        self.animation.start(self.icons[0])
        Clock.schedule_once(lambda *args: self.animation.start(self.icons[1]), 0.3)
        Clock.schedule_once(lambda *args: self.animation.start(self.icons[2]), 0.7)

    def stop_animation(self):
        for icon in self.icons:
            self.animation.stop(icon)
