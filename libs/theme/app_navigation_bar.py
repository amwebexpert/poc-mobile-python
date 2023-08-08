import logging

from kivy.uix.screenmanager import ScreenManager

from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer

from libs.utils.app_utils import bus

class AppNavigationBar(MDTopAppBar):
    nav_drawer: MDNavigationDrawer
    screen_manager: ScreenManager

    screens_stack: list[str]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.screens_stack = []
    
    def close_menu(self) -> None:
        self.nav_drawer.set_state("close")

    def on_menu_action(self, *args) -> None:
        self.nav_drawer.set_state("open")

    def on_settings_action(self, *args) -> None:
        self.navigate_to("settings")

    def can_go_back(self) -> bool:
        return len(self.screens_stack) > 1
    
    def get_current_screen(self) -> str:
        if not self.screens_stack:
            return None
        return self.screens_stack[-1]

    def navigate_to(self, screen_name: str) -> None:
        self.close_menu()
        if screen_name == self.get_current_screen():
            logging.error(f"Screen <{screen_name}> already on top of the stack.")
            return
        self.screens_stack.append(screen_name)
        if self.screen_manager.current != screen_name:
            self.screen_manager.transition.direction = 'left'
            self.screen_manager.current = screen_name
        self.update_menu_icons_and_actions()

    def update_menu_icons_and_actions(self) -> None:
        if self.get_current_screen() == "home":
            self.left_action_items = [["menu", lambda x: self.on_menu_action()]]
            self.right_action_items = [["cog", lambda x: self.on_settings_action()]]
        else:
            self.left_action_items = [["arrow-left", lambda x: self.go_back()]]
            self.right_action_items = []

    def go_back(self) -> None:
        if not self.can_go_back():
            logging.error("No screens to pop.")
            return
        self.screens_stack.pop()
        self.screen_manager.transition.direction = 'right'
        self.screen_manager.current = self.get_current_screen()
        self.update_menu_icons_and_actions()
