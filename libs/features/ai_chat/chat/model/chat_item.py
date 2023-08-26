from datetime import datetime

from enum import Enum

ChatItemRole = Enum("ChatItemRole", ["me", "AI"])


class ChatItem:  # pylint: disable=too-few-public-methods
    id: int
    chat_session_id: int
    iso_created_at: str
    description: str
    role: int = ChatItemRole.me.value

    def __init__(self,  # pylint: disable=too-many-arguments
                 chat_session_id: int,
                 description: str,
                 role: int = ChatItemRole.me.value,
                 iso_created_at: str = None,
                 id: int = 0  # pylint: disable=redefined-builtin, invalid-name
                 ) -> None:
        self.chat_session_id = chat_session_id
        self.description = description
        self.role = role
        self.id = id  # pylint: disable=redefined-builtin, invalid-name
        self.iso_created_at = iso_created_at

        # override None values with defaults
        if self.iso_created_at is None:
            self.iso_created_at = datetime.utcnow().isoformat()
