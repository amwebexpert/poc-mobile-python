import logging

from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer


class AppNavigationBar(MDTopAppBar):  # pylint: disable=too-many-ancestors
    nav_drawer: MDNavigationDrawer
    screen_manager: ScreenManager

    screens_stack: list[str]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.screens_stack = []
        Window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, _window, key, *_args) -> bool:
        if key == 27:
            if self.nav_drawer.state == "open":
                self.close_menu()
            elif self.can_go_back():
                self.go_back()
            else:
                MDApp.get_running_app().stop()
            return True
        return False

    def close_menu(self) -> None:
        self.nav_drawer.set_state("close")

    def on_menu_action(self, *_args) -> None:
        self.nav_drawer.set_state("open")

    def on_settings_action(self, *_args) -> None:
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
            logging.error(
                "Screen <%s> already on top of the stack.", screen_name)
            return
        self.screens_stack.append(screen_name)
        if self.screen_manager.current != screen_name:
            self.screen_manager.transition.direction = 'left'
            self.screen_manager.current = screen_name
        self.update_menu_icons_and_actions()

    def update_menu_icons_and_actions(self) -> None:
        if self.get_current_screen() == "settings":
            self.right_action_items = []
        else:
            self.right_action_items = [
                ["cog", lambda x: self.on_settings_action()]]

        if self.can_go_back():
            self.left_action_items = [["arrow-left", lambda x: self.go_back()]]
        else:
            self.left_action_items = [
                ["menu", lambda x: self.on_menu_action()]]

    def go_back(self) -> None:
        if not self.can_go_back():
            logging.error("No screens to pop.")
            return
        self.screens_stack.pop()
        self.screen_manager.transition.direction = 'right'
        self.screen_manager.current = self.get_current_screen()
        self.update_menu_icons_and_actions()
