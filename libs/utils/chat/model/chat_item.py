from datetime import datetime

from enum import Enum

ChatItemRole = Enum("ChatItemRole", ["me", "AI"])

class ChatItem:
    id = 0
    chat_session_id = 0
    iso_created_at = ""
    description = ""
    role = ChatItemRole.me.value

    def __init__(self, chat_session_id = 0, iso_created_at = datetime.utcnow().isoformat() , description = "", role = ChatItemRole.me.value) -> None:
        self.chat_session_id = chat_session_id
        self.iso_created_at = iso_created_at
        self.description = description
        self.role = role
