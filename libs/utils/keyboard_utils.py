from kivy.core.window import Window

# see https://youtube.com/watch?v=sa4AVMjjzNo
# https://kivy.org/doc/stable/api-kivy.core.window.html#kivy.core.window.WindowBase.softinput_mode
def init_keyboard() -> None:
    Window.keyboard_anim_args = {'d': 0.2, 't': 'in_out_expo'}
    Window.softinput_mode = "below_target"
