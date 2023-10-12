import os
from typing import Union
from kivy.animation import Animation, AnimationTransition
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import (
    AliasProperty,
    BooleanProperty,
    ColorProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    StringProperty,
    VariableListProperty,
)
from kivymd.uix.boxlayout import MDBoxLayout

# taken directly from MDNavigationDrawerHeader in /kivymd/uix/navigationdrawer/navigationdrawer.py
class MDNavigationDrawerHeaderOM(MDBoxLayout):
    """
    Implements a header for a menu for :class:`~MDNavigationDrawer` class.

    For more information, see in the :class:`~kivymd.uix.boxlayout.MDBoxLayout`
    class documentation.

    .. versionadded:: 1.0.0

    .. code-block:: kv

        MDNavigationDrawer:

            MDNavigationDrawerMenu:

                MDNavigationDrawerHeader:
                    title: "Header title"
                    text: "Header text"
                    spacing: "4dp"
                    padding: "12dp", 0, 0, "56dp"

    .. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/navigation-drawer-header.png
        :align: center
    """

    source = StringProperty()
    """
    Image logo path.

    .. code-block:: kv

        MDNavigationDrawer:

            MDNavigationDrawerMenu:

                MDNavigationDrawerHeader:
                    title: "Header title"
                    text: "Header text"
                    source: "logo.png"
                    spacing: "4dp"
                    padding: "12dp", 0, 0, "56dp"

    .. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/navigation-drawer-header-source.png
        :align: center

    :attr:`source` is a :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """

    title = StringProperty()
    """
    Title shown in the first line.

    :attr:`title` is a :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """

    title_halign = StringProperty("left")
    """
    Title halign first line.

    :attr:`title_halign` is a :class:`~kivy.properties.StringProperty`
    and defaults to `'left'`.
    """

    title_color = ColorProperty(None)
    """
    Title text color in (r, g, b, a) or string format.

    :attr:`title_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    title_font_style = StringProperty("H4")
    """
    Title shown in the first line.

    :attr:`title_font_style` is a :class:`~kivy.properties.StringProperty`
    and defaults to `'H4'`.
    """

    title_font_size = StringProperty("34sp")
    """
    Title shown in the first line.

    :attr:`title_font_size` is a :class:`~kivy.properties.StringProperty`
    and defaults to `'34sp'`.
    """

    text = StringProperty()
    """
    Text shown in the second line.

    :attr:`text` is a :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """

    text_halign = StringProperty("left")
    """
    Text halign first line.

    :attr:`text_halign` is a :class:`~kivy.properties.StringProperty`
    and defaults to `'left'`.
    """

    text_color = ColorProperty(None)
    """
    Title text color in (r, g, b, a) or string format.

    :attr:`text_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    text_font_style = StringProperty("H6")
    """
    Title shown in the first line.

    :attr:`text_font_style` is a :class:`~kivy.properties.StringProperty`
    and defaults to `'H6'`.
    """

    text_font_size = StringProperty("20sp")
    """
    Title shown in the first line.

    :attr:`text_font_size` is a :class:`~kivy.properties.StringProperty`
    and defaults to `'20sp'`.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.check_content)

    def check_content(self, interval: Union[int, float]) -> None:
        """Removes widgets that the user has not added to the container."""

        if not self.title:
            self.ids.label_box.remove_widget(self.ids.title)
        if not self.text:
            self.ids.label_box.remove_widget(self.ids.text)
        if not self.source:
            self.remove_widget(self.ids.logo)