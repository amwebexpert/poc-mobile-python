from datetime import datetime
from typing import List

from libs.utils.chat.model.chat_item import ChatItem

class ChatSession:
    id: int
    iso_created_at: str
    title: str
    items: List[ChatItem] = []

    def __init__(self, title: str, items: List[ChatItem] = [], iso_created_at: str = datetime.utcnow().isoformat(), id: int = 0) -> None:
        self.id = id
        self.iso_created_at = iso_created_at
        self.title = title
        self.items = items
