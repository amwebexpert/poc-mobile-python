import logging
from datetime import datetime

from kivymd.uix.widget import Widget
from kivymd.uix.menu import MDDropdownMenu

from kivy.clock import Clock
from kivy.animation import Animation
from kivy.factory import Factory

from libs.theme.base_screen import BaseScreen

from libs.utils.app_utils import bus
from libs.utils.preferences_service import PreferencesService, Preferences
from libs.utils.chat.chat_session_service import ChatSessionService
from libs.utils.chat.model.chat_session import ChatSession
from libs.utils.chat.model.chat_item import ChatItem, ChatItemRole

from libs.utils.chat_gpt_service import ChatGptService
from libs.utils.string_utils import is_blank
from libs.utils.keyboard_utils import has_soft_keyboard
from libs.theme.theme_utils import AnimatedIcons

CHAT_DATETIME_FORMAT = "%m-%d-%Y %H:%M"

class HomeScreen(BaseScreen):
    chat_session_service: ChatSessionService = None
    preferences_service: PreferencesService = None
    chat_gpt_service: ChatGptService = None

    chat_session: ChatSession = ChatSession()
    user_chat_item: ChatItem = None

    animatedIcons: AnimatedIcons = None

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.chat_session_service = ChatSessionService()
        self.preferences_service = PreferencesService()
        self.chat_gpt_service = ChatGptService(
            api_key = self.preferences_service.get(Preferences.OPEN_AI_KEY.name),
            ai_system_initial_context = self.preferences_service.get(Preferences.AI_SYSTEM_INITIAL_CONTEXT.name),
            temperature = float(self.preferences_service.get(Preferences.AI_TEMPERATURE.name, 0))
        )
        self.animatedIcons = AnimatedIcons()
        Clock.schedule_once(self.init_chat_history, 0)
        Clock.schedule_once(self.init_sessions_drop_down_menu, 0)

    def get_chat_session_title(self) -> Widget:
        return self.getUIElement("chat_session_label")

    def init_sessions_drop_down_menu(self, *args) -> None:
        chat_sessions = self.chat_session_service.get_all_sessions()
        items = [
            {
                "text": chat_session.title,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=chat_session: self.on_chat_session_selected(x),
            } for chat_session in chat_sessions
        ]
        self.menu = MDDropdownMenu(caller = self.get_chat_session_title(), items = items, width_mult = 10)

    def open_chat_sessions_menu(self) -> None:
        self.menu.open()
    
    def on_chat_session_selected(self, chat_session: ChatSession) -> None:
        self.get_chat_session_title().text = chat_session.title
        self.chat_session = self.chat_session_service.get(chat_session.id)
        self.chat_gpt_service.resume_existing_session(self.chat_session)
        self.recreate_chat_list_from_session()
        self.menu.dismiss()
    
    def on_new_chat_session(self, *args) -> None:
        self.chat_session = ChatSession()
        self.chat_session = self.chat_session_service.save(self.chat_session)
        self.get_chat_session_title().text = self.chat_session.title
        self.chat_gpt_service.resume_existing_session(self.chat_session)
        self.recreate_chat_list_from_session()
    
    def recreate_chat_list_from_session(self) -> None:
        self.getUIElement("chat_list").clear_widgets()
        for chat_item in self.chat_session.items:
            if int(chat_item.role) == ChatItemRole.me.value:
                self.getUIElement("chat_list").add_widget(self.buildChatItemRight(text=chat_item.description, created_at=chat_item.iso_created_at))
            else:
                self.getUIElement("chat_list").add_widget(self.buildChatItemLeft(text=chat_item.description, created_at=chat_item.iso_created_at))

    def add_animation(self, *args) -> None:
        self.getUIElement("chat_list").add_widget(self.animatedIcons.widget)
        self.getUIElement("chat_scroll").scroll_to(self.animatedIcons.widget)
        self.animatedIcons.start_animation()

    def remove_animation(self, *args) -> None:
        self.animatedIcons.stop_animation()
        self.getUIElement("chat_list").remove_widget(self.animatedIcons.widget)

    def init_chat_history(self, *args) -> None:
        item = self.buildChatItemLeft("I'm an artificial intelligence helpful assistant. How can I help you?")
        self.getUIElement("chat_list").add_widget(item)

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

    def send_message(self, text: str) -> None:
        if is_blank(text):
            return

        api_key = self.preferences_service.get(Preferences.OPEN_AI_KEY.name)
        if is_blank(api_key):
            self.getUIElement("chat_list").add_widget(self.buildChatItemLeft("Missing OpenAI API key. Please set it in the settings screen."))
            return

        self.chat_gpt_service.set_api_key(api_key)
        self.chat_gpt_service.send_message(text, on_success=self.on_success, on_error=self.on_error)

        self.user_chat_item = ChatItem(chat_session_id=self.chat_session.id, description=text, role=ChatItemRole.me.value)
        self.getUIElement("chat_list").add_widget(self.buildChatItemRight(text))
        self.add_animation()
    
    def reset_input_and_set_focus(self, clear_text: bool = True) -> None:
        chat_input = self.getUIElement("chat_input_text")
        if clear_text:
            chat_input.text = ""
        if not has_soft_keyboard():
            chat_input.focus = True
    
    def on_success(self, response_message: str) -> None:
        self.remove_animation()

        if not self.chat_session.has_items():
            self.chat_gpt_service.generate_summary_title(question=self.user_chat_item.description, on_success=self.update_session_title)

        ai_chat_item = ChatItem(chat_session_id=self.chat_session.id, description=response_message, role=ChatItemRole.AI.value)
        self.chat_session.items.append(self.user_chat_item)
        self.chat_session.items.append(ai_chat_item)
        self.chat_session = self.chat_session_service.save(chat_session=self.chat_session)

        self.reset_input_and_set_focus()
        self.getUIElement("chat_list").add_widget(self.buildChatItemLeft(response_message))

    def update_session_title(self, title: str) -> None:
        self.chat_session.title = f"{title} ({self.chat_session.title})"
        self.chat_session_service.update_chat_session_title(self.chat_session)
        self.init_sessions_drop_down_menu()
        self.get_chat_session_title().text = self.chat_session.title

    def on_error(self, error_message: str) -> None:
        self.remove_animation()
        self.reset_input_and_set_focus(clear_text=False)
        self.getUIElement("chat_list").add_widget(self.buildChatItemLeft(error_message))

    @bus.on("app_started_event")
    def handle_app_started_event(info: str = "") -> None:
        logging.debug(f"HomeScreen: App <{info}> started.")
