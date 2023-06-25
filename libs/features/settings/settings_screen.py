from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.widget import Widget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.menu import MDDropdownMenu

from kivy.lang import Builder
from kivy.clock import Clock
from libs.utils.app_utils import get_app_screen
  
Builder.load_file('libs/features/settings/settings_screen.kv')

PRIMARY_COLORS = ['Red' , 'Pink' , 'Purple' , 'DeepPurple' , 'Indigo' , 'Blue' , 'LightBlue' , 'Cyan' , 'Teal' , 'Green' , 'LightGreen' , 'Lime' , 'Yellow' , 'Amber' , 'Orange' , 'DeepOrange' , 'Brown' , 'Gray' , 'BlueGray']

class SettingsScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.init_primary_colors_drop_down_list, 0)
    
    def init_primary_colors_drop_down_list(self, *args):
        screen = get_app_screen("settings")
        primary_color_menu_button = screen.ids['primary_color_menu_button']
        menu_items = [
            {
                "text": color,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=color: self.on_color_selected(x),
            } for color in PRIMARY_COLORS
        ]
        self.menu = MDDropdownMenu(
            caller = primary_color_menu_button,
            items = menu_items,
            width_mult = 4,
        )

    def open_color_menu(self):
        self.menu.open()
    
    def on_color_selected(self, color):
        theme = MDApp.get_running_app().theme_cls
        theme.primary_palette = color
        self.menu.dismiss()

    def toggle_theme(self):
        theme = MDApp.get_running_app().theme_cls
        if theme.theme_style == "Dark":
            theme.theme_style = "Light"
        else:
            theme.theme_style = "Dark"
