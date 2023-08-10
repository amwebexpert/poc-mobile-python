from datetime import datetime

from kivymd.uix.widget import Widget
from kivymd.uix.menu import MDDropdownMenu

from kivy.clock import Clock
from kivy.factory import Factory

from libs.theme.base_screen import BaseScreen

from libs.features.settings.preferences_service import PreferencesService, Preferences
from libs.features.ai_text_to_img.text2img_service import Text2ImgService
from libs.features.ai_text_to_img.model.text2img_session import Text2ImgSession
from libs.features.ai_text_to_img.image_creator_service import ImageCreatorService

from libs.utils.string_utils import is_blank
from libs.utils.keyboard_utils import has_soft_keyboard

from libs.theme.theme_utils import AnimatedIcons

CHAT_DATETIME_FORMAT = "%Y-%m-%d %H:%M"

class Text2ImgScreen(BaseScreen):
    session_service: Text2ImgService = None
    preferences_service: PreferencesService = None
    image_creator_service: ImageCreatorService = None

    session: Text2ImgSession = Text2ImgSession()

    animatedIcons: AnimatedIcons = None

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.session_service = Text2ImgService()
        self.preferences_service = PreferencesService()
        self.image_creator_service = ImageCreatorService()
        self.animatedIcons = AnimatedIcons()
        Clock.schedule_once(self.init_text2img_history, 0)
        Clock.schedule_once(self.init_sessions_drop_down_menu, 0)

    def get_session_title(self) -> Widget:
        return self.getUIElement("text2img_session_label")

    def init_sessions_drop_down_menu(self, *args) -> None:
        text2img_sessions = self.session_service.get_all_sessions()
        items = [
            {
                "text": session.query,
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
        self.recreate_text2img_list_from_session()
        self.menu.dismiss()

    def recreate_text2img_list_from_session(self) -> None:
        text2img_list = self.getUIElement("text2img_list")
        text2img_list.clear_widgets() # normally this would be enough

        text2img_list.add_widget(self.buildChatItemRight(text=self.session.query, created_at=self.session.iso_created_at))
        text2img_list.add_widget(self.buildChatItemLeft(text=self.session.base64, created_at=self.session.iso_response_received_at))

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
        return self.buildChatItem(chatItem=Factory.AdaptativeLabelBoxRight(), text=text, role="user", created_at=created_at)
    
    def buildChatItemLeft(self, text: str, created_at: str = None) -> Widget:
        return self.buildChatItem(chatItem=Factory.AdaptativeLabelBoxLeft(), text=text, role="assistant", created_at=created_at)

    def buildChatItem(self, chatItem: Widget, text: str, role: str, created_at: str = None) -> Widget:
        timestamp = datetime.now() if created_at is None else datetime.fromisoformat(created_at)
        chatItem.ids.label.text = text
        chatItem.ids.created_at.text = timestamp.strftime(CHAT_DATETIME_FORMAT)
        chatItem.ids.created_at.icon = "human-greeting-variant" if role == "user" else "robot-outline"
        return chatItem

    def send_message(self, query: str) -> None:
        if is_blank(query):
            return

        api_key = self.preferences_service.get(Preferences.OPEN_AI_KEY.name)
        if is_blank(api_key):
            self.getUIElement("text2img_list").add_widget(self.buildChatItemLeft("Missing Stability API key. Please set it in the settings screen."))
            return

        self.image_creator_service.set_api_key(api_key)
        self.image_creator_service.send_message(query, on_success=self.on_success, on_error=self.on_error)

        self.session = Text2ImgSession(query=query)
        self.getUIElement("text2img_list").add_widget(self.buildChatItemRight(query))
        self.add_animation()
    
    def reset_input_and_set_focus(self, clear_text: bool = True) -> None:
        text2img_input = self.getUIElement("text2img_input_text")
        if clear_text:
            text2img_input.text = ""
        if not has_soft_keyboard():
            text2img_input.focus = True
    
    def on_success(self, base64: str) -> None:
        self.remove_animation()

        self.session.base64 = base64
        self.session.iso_response_received_at = datetime.utcnow().isoformat()
        self.session = self.session_service.save(self.session)
        self.get_session_title().text = datetime.now().strftime(CHAT_DATETIME_FORMAT)
        self.recreate_text2img_list_from_session()

        self.reset_input_and_set_focus()
        self.getUIElement("text2img_list").add_widget(self.buildChatItemLeft(base64))

    def on_error(self, error_message: str) -> None:
        self.remove_animation()
        self.reset_input_and_set_focus(clear_text=False)
        self.getUIElement("text2img_list").add_widget(self.buildChatItemLeft(error_message))
