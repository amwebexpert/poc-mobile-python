from datetime import datetime
from typing import List

from libs.features.ai_chat.chat.model.chat_item import ChatItem

CHAT_DATETIME_FORMAT = "%Y-%m-%d %H:%M"


class ChatSession:
    id: int
    iso_created_at: str
    title: str
    items: List[ChatItem] = []

    def __init__(self,
                 title: str = None,
                 items: List[ChatItem] = None,
                 iso_created_at: str = None,
                 id: int = 0  # pylint: disable=redefined-builtin, invalid-name
                 ) -> None:
        self.id = id  # pylint: disable=redefined-builtin, invalid-name
        self.items = [] if items is None else items
        self.iso_created_at = iso_created_at
        self.title = title

        # override None values with defaults
        if self.iso_created_at is None:
            self.iso_created_at = datetime.utcnow().isoformat()
        if self.title is None:
            self.title = datetime.now().strftime(CHAT_DATETIME_FORMAT)

    def has_items(self) -> bool:
        return len(self.items) > 0

    def __str__(self):
        return f"ChatSession(id={self.id}, title={self.title}, items={self.items}, iso_created_at={self.iso_created_at})"
