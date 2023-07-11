from datetime import datetime

from kivymd.uix.screen import MDScreen

from kivy.clock import Clock
from kivy.animation import Animation
from kivy.factory import Factory

from libs.utils.preferences_service import PreferencesService, Preferences
from libs.utils.chat_gpt_service import ChatGptService
from libs.utils.screen_utils import is_mobile
  
class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.preferences_service = PreferencesService()
        self.chat_gpt_service = ChatGptService(
            api_key = self.preferences_service.get(Preferences.OPEN_AI_KEY.name),
            ai_system_initial_context = self.preferences_service.get(Preferences.AI_SYSTEM_INITIAL_CONTEXT.name),
            temperature = float(self.preferences_service.get(Preferences.AI_TEMPERATURE.name, 0))
        )
        self.init_chat_animation()
        Clock.schedule_once(self.init_chat_history, 0)

    def init_chat_animation(self, *args):
        self.animated_layout = Factory.AnimatedIconButton()
        self.animation = Animation(opacity=0, d=0.7) + Animation(opacity=1, d=0.7)
        self.animation.repeat = True

    def add_animation(self, *args):
        self.getUIElement("chat_list").add_widget(self.animated_layout)
        icons = self.animated_layout.ids
        self.animation.start(icons.animated_icon)
        Clock.schedule_once(lambda *args: self.animation.start(icons.animated_icon_2), 0.7)
        Clock.schedule_once(lambda *args: self.animation.start(icons.animated_icon_3), 0.3)
        self.getUIElement("chat_scroll").scroll_to(self.animated_layout)

    def remove_animation(self, *args):
        icons = self.animated_layout.ids
        self.animation.stop(icons.animated_icon)
        self.animation.stop(icons.animated_icon_2)
        self.animation.stop(icons.animated_icon_3)
        self.getUIElement("chat_list").remove_widget(self.animated_layout)

    def getUIElement(self, name):
        screen = self.manager.get_screen("home")
        return screen.ids[name]

    def init_chat_history(self, *args):
        item = self.buildChatItemLeft("I'm an artificial intelligence helpful assistant. How can I help you?")
        self.getUIElement("chat_list").add_widget(item)

    def buildChatItemRight(self, text):
        return self.buildChatItem(chatItem=Factory.AdaptativeLabelBoxRight(), text=text, role="user")
    
    def buildChatItemLeft(self, text):
        return self.buildChatItem(chatItem=Factory.AdaptativeLabelBoxLeft(), text=text, role="assistant")

    def buildChatItem(self, chatItem, text, role):
        chatItem.ids.label.text = text
        chatItem.ids.created_at.icon = "human-greeting-variant" if role == "user" else "robot-outline"
        chatItem.ids.created_at.text = datetime.now().strftime("%m-%d-%Y %H:%M")
        return chatItem

    def send_message(self, text):
        api_key = self.preferences_service.get(Preferences.OPEN_AI_KEY.name)
        if (api_key == None):
            self.getUIElement("chat_list").add_widget(self.buildChatItemLeft("Missing OpenAI API key. Please set it in the settings screen."))
            return
        self.chat_gpt_service.send_message(text, on_success=self.on_success, on_error=self.on_error)
        self.getUIElement("chat_list").add_widget(self.buildChatItemRight(text))
        self.add_animation()
    
    def reset_input_and_set_focus(self, clearText = False):
        chat_input = self.getUIElement("chat_input_text")
        chat_input.text = ""
        if not is_mobile():
            chat_input.focus = True
    
    def on_success(self, responseMessage):
        self.remove_animation()
        self.reset_input_and_set_focus()
        self.getUIElement("chat_list").add_widget(self.buildChatItemLeft(responseMessage))

    def on_error(self, errorMessage):
        self.remove_animation()
        self.reset_input_and_set_focus(clearText=False)
        self.getUIElement("chat_list").add_widget(self.buildChatItemLeft(errorMessage))
