from kivy.core.window import Window

from libs.utils.platform_utils import is_android, is_ios

# see https://youtube.com/watch?v=sa4AVMjjzNo
# https://kivy.org/doc/stable/api-kivy.core.window.html#kivy.core.window.WindowBase.softinput_mode

KEY_VALUE_ESCAPE = 27  # also mapped to Android back button


def init_keyboard() -> None:
    Window.keyboard_anim_args = {"d": 0.2, "t": "in_out_expo"}
    Window.softinput_mode = "below_target"


def has_soft_keyboard() -> bool:
    return is_android() or is_ios()
