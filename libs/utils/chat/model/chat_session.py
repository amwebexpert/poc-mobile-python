from datetime import datetime
from typing import List

from libs.utils.chat.model.chat_item import ChatItem

class ChatSession:
    id: int
    iso_created_at: str
    title: str
    items: List[ChatItem] = []

    def __init__(self, 
            title: str = None,
            items: List[ChatItem] = [],
            iso_created_at: str = None,
            id: int = 0
        ) -> None:
        self.id = id
        self.items = items
        self.iso_created_at = iso_created_at
        self.title = title

        # override None values with defaults
        if self.iso_created_at is None:
            self.iso_created_at = datetime.utcnow().isoformat()
        if self.title is None:
            self.title = datetime.now().strftime("%m-%d-%Y %H:%M")

def __str__(self):
     return f"ChatSession(id={self.id}, title={self.title}, items={self.items}, iso_created_at={self.iso_created_at})"
