from kivymd.app import MDApp

def get_app_screen(screen_name):
    app = MDApp.get_running_app()
    screen_manager = app.root.ids.screen_manager
    return screen_manager.get_screen(screen_name)
