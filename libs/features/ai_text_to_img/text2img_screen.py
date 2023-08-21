from datetime import datetime
import base64
from pathlib import Path

from kivy.clock import Clock
from kivy.factory import Factory

from kivymd.uix.widget import Widget
from kivymd.uix.menu import MDDropdownMenu

from libs.theme.base_screen import BaseScreen

from libs.features.settings.preferences_service import PreferencesService, Preferences
from libs.features.ai_text_to_img.text2img_service import Text2ImgService
from libs.features.ai_text_to_img.model.text2img_session import Text2ImgSession
from libs.features.ai_text_to_img.image_creator_service import ImageCreatorService

from libs.utils.string_utils import is_blank
from libs.utils.keyboard_utils import has_soft_keyboard
from libs.utils.date_utils import get_tz_delta

from libs.theme.theme_utils import AnimatedIcons

CHAT_DATETIME_FORMAT = "%Y-%m-%d %H:%M"

class Text2ImgScreen(BaseScreen):
    session_service: Text2ImgService = None
    preferences_service: PreferencesService = None
    image_creator_service: ImageCreatorService = None

    session: Text2ImgSession = Text2ImgSession()

    animatedIcons = AnimatedIcons()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.session_service = Text2ImgService()
        self.preferences_service = PreferencesService()
        self.image_creator_service = ImageCreatorService()
        Clock.schedule_once(self.init_text2img_history, 0)
        Clock.schedule_once(self.init_sessions_drop_down_menu, 0)

    def get_session_title(self) -> Widget:
        return self.getUIElement("text2img_session_label")

    def init_sessions_drop_down_menu(self, *args) -> None:
        text2img_sessions = self.session_service.get_all_sessions()
        items = [
            {
                "text": self.build_title_from_session(session),
                "viewclass": "OneLineListItem",
                "on_release": lambda x=session: self.on_session_selected(x),
            } for session in text2img_sessions
        ]
        self.menu = MDDropdownMenu(caller = self.get_session_title(), items = items, width_mult = 10)

    def open_sessions_menu(self) -> None:
        self.menu.open()

    def on_session_selected(self, session: Text2ImgSession) -> None:
        self.get_session_title().text = session.query
        self.session = self.session_service.get(session.id)
        self.recreate_text2img_list_from_session(clearAll=True)
        self.menu.dismiss()
    
    def build_title_from_session(self, session: Text2ImgSession) -> str:
        title = session.query[0:30]
        if (len(session.query) > len(title)):
            title += "…"
        return title

    def recreate_text2img_list_from_session(self, clearAll: bool = False) -> None:
        text2img_list = self.getUIElement("text2img_list")
        if clearAll:
            text2img_list.clear_widgets()

        text2img_list.add_widget(self.buildChatItemRight(text=self.session.query, created_at=self.session.iso_created_at))
        if self.session.iso_response_received_at is not None:
            session = self.session
            text2img_list.add_widget(self.buildChatImageItemLeft(base_64_data=session.base64, base_64_seed=session.base64_seed, date_and_time=session.iso_response_received_at))

    def add_animation(self, *args) -> None:
        self.getUIElement("text2img_list").add_widget(self.animatedIcons.widget)
        self.getUIElement("text2img_scroll").scroll_to(self.animatedIcons.widget)
        self.animatedIcons.start_animation()

    def remove_animation(self, *args) -> None:
        self.animatedIcons.stop_animation()
        self.getUIElement("text2img_list").remove_widget(self.animatedIcons.widget)

    def init_text2img_history(self, *args) -> None:
        item = self.buildChatItemLeft("I'm an artificial intelligence image generator. Describe the image to generate.")
        self.getUIElement("text2img_list").add_widget(item)
        self.getUIElement("text2img_scroll").scroll_to(item)

    def buildChatItemRight(self, text: str, created_at: str = None) -> Widget:
        return self.buildChatItem(chatItem=Factory.AdaptativeLabelBoxRight(), text=text, role="user", date_and_time=created_at)
    
    def buildChatItemLeft(self, text: str, created_at: str = None) -> Widget:
        return self.buildChatItem(chatItem=Factory.AdaptativeLabelBoxLeft(), text=text, role="assistant", date_and_time=created_at)

    def buildChatItem(self, chatItem: Widget, text: str, role: str, date_and_time: str = None) -> Widget:
        timestamp = datetime.now() if date_and_time is None else datetime.fromisoformat(date_and_time) + get_tz_delta()
        chatItem.ids.label.text = text
        chatItem.ids.created_at.text = timestamp.strftime(CHAT_DATETIME_FORMAT)
        chatItem.ids.created_at.icon = "human-greeting-variant" if role == "user" else "robot-outline"
        return chatItem

    def buildChatImageItemLeft(self, base_64_data: str, base_64_seed: str, date_and_time: str = None) -> Widget:
        timestamp = datetime.now() if date_and_time is None else datetime.fromisoformat(date_and_time) + get_tz_delta()
        image_path_and_name = self.write_image_data_to_file(base_64_data=base_64_data, base_64_seed=base_64_seed)

        chatItem = Factory.AdaptativeImageBoxLeft()
        chatItem.ids.created_at.icon = "robot-outline"
        chatItem.ids.created_at.text = timestamp.strftime(CHAT_DATETIME_FORMAT)
        chatItem.ids.generated_image.source = image_path_and_name

        return chatItem

    def write_image_data_to_file(self, base_64_data: str, base_64_seed: str):
        image_path = "generated-images"
        image_path_and_name = f"{image_path}/image-{base_64_seed}.png" # TODO use os.path.join instead

        Path(image_path).mkdir(parents=True, exist_ok=True)
        with open(image_path_and_name, "wb") as f:
            decoded_image_data = base64.decodebytes(base_64_data.encode())
            f.write(decoded_image_data)

        return image_path_and_name

    def send_message(self, query: str) -> None:
        if is_blank(query):
            return

        api_key = self.preferences_service.get(Preferences.STABILITY_AI_KEY.name)
        if is_blank(api_key):
            self.getUIElement("text2img_list").add_widget(self.buildChatItemLeft("Missing Stability API key. Please set it in the settings screen."))
            return

        self.session = Text2ImgSession(query=query)
        self.getUIElement("text2img_list").add_widget(self.buildChatItemRight(query))
        self.add_animation()

        self.image_creator_service.set_api_key(api_key)
        self.image_creator_service.send_message(self.session.query, on_success=self.on_success, on_error=self.on_error)

    def reset_input_and_set_focus(self, clear_text: bool = True) -> None:
        text2img_input = self.getUIElement("text2img_input_text")
        if clear_text:
            text2img_input.text = ""
        if not has_soft_keyboard():
            text2img_input.focus = True
    
    def on_success(self, base64: str, base_64_seed: str) -> None:
        self.remove_animation()

        self.session.base64 = base64
        self.session.base64_seed = base_64_seed
        self.session.iso_response_received_at = datetime.utcnow().isoformat()
        self.session = self.session_service.save(self.session)

        text2img_list = self.getUIElement("text2img_list")
        session = self.session
        text2img_list.add_widget(self.buildChatImageItemLeft(base_64_data=session.base64, base_64_seed=session.base64_seed, date_and_time=session.iso_response_received_at))

        self.init_sessions_drop_down_menu()
        self.get_session_title().text = self.build_title_from_session(self.session)

        self.reset_input_and_set_focus()

    def on_error(self, error_message: str) -> None:
        self.remove_animation()
        self.reset_input_and_set_focus(clear_text=False)
        self.getUIElement("text2img_list").add_widget(self.buildChatItemLeft(error_message))
