from datetime import datetime

from enum import Enum

ChatItemRole = Enum("ChatItemRole", ["me", "AI"])

class ChatItem:
    id: int
    chat_session_id: int
    iso_created_at: str
    description: str
    role: int = ChatItemRole.me.value

    def __init__(self, chat_session_id: int, description: str, role: int = ChatItemRole.me.value, iso_created_at: str = datetime.utcnow().isoformat()) -> None:
        self.chat_session_id = chat_session_id
        self.iso_created_at = iso_created_at
        self.description = description
        self.role = role
