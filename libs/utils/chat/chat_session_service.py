from typing import List

from libs.utils.storage_service import StorageService
from libs.utils.chat.model.chat_session import ChatSession
from libs.utils.chat.model.chat_item import ChatItem

class ChatSessionService:
    def __init__(self) -> None:
        self.storage_service = StorageService("chat_sessions.db")
        self.storage_service.connect()
        self.create_chat_session_table()
        self.create_chat_session_items_table()
        self.storage_service.close()
    
    def create_chat_session_table(self) -> None:
        self.storage_service.create_table(
            table_name = "chat_sessions", 
            columns=(
                "id              INTEGER PRIMARY KEY AUTOINCREMENT",
                "iso_created_at  TEXT NOT NULL",
                "title           TEXT NOT NULL"
            )
        )
    
    def create_chat_session_items_table(self) -> None:
        self.storage_service.create_table(
            table_name = "chat_session_items", 
            columns=(
                "id              INTEGER PRIMARY KEY AUTOINCREMENT",
                "chat_session_id INTEGER NOT NULL",
                "iso_created_at  TEXT NOT NULL",
                "description     TEXT NOT NULL",
                "role            INTEGER NOT NULL"
            )
        )
    
    def get_all_sessions(self) -> List[ChatSession]:
        self.storage_service.connect()
        result = self.storage_service.select("chat_sessions", ["*"])
        chat_sessions = []
        for chat_session_rs in result:
            chat_session = ChatSession(id = chat_session_rs[0], iso_created_at = chat_session_rs[1], title = chat_session_rs[2])
            chat_sessions.append(chat_session)
        self.storage_service.close()
        chat_sessions.sort(key=lambda session: session.iso_created_at, reverse=True)
        return chat_sessions

    def save(self, chat_session: ChatSession) -> ChatSession:
        self.storage_service.connect()

        if chat_session.id == 0:
            chat_session.id = self.create(chat_session)

        for chat_item in chat_session.items:
            if chat_item.id == 0:
                chat_item.id = self.add_chat_session_item(chat_session, chat_item)

        self.storage_service.close()
        return chat_session

    def add_chat_session_item(self, chat_session: ChatSession, chat_item: ChatItem) -> int:
        chat_item.id = self.storage_service.insert(
            table_name="chat_session_items", 
            columns=("chat_session_id", "iso_created_at", "description", "role"),
            values=(chat_session.id, chat_item.iso_created_at, chat_item.description, chat_item.role)
        )
        return chat_item.id

    def create(self, chat_session: ChatSession) -> int:
        chat_session.id = self.storage_service.insert(
            table_name="chat_sessions", 
            columns=("iso_created_at", "title"),
            values=(chat_session.iso_created_at, chat_session.title)
        )
        return chat_session.id

    def get(self, id = 0) -> ChatSession:
        self.storage_service.connect()
        result = self.storage_service.select("chat_sessions", ["*"], f"id = {id}")
        if len(result) == 0:
            return None

        chat_session_rs = result[0]
        chat_session = ChatSession(title = chat_session_rs[2], items = [], iso_created_at = chat_session_rs[1], id = chat_session_rs[0])
        self.load_chat_session_items(chat_session)
        self.storage_service.close()
        return chat_session
    
    def load_chat_session_items(self, chat_session: ChatSession) -> None:
        result = self.storage_service.select("chat_session_items", ["*"], f"chat_session_id = {chat_session.id}")
        for chat_session_item_rs in result:
            chat_session.items.append(
                ChatItem(
                    id = chat_session_item_rs[0],
                    chat_session_id = chat_session_item_rs[1],
                    iso_created_at = chat_session_item_rs[2],
                    description = chat_session_item_rs[3],
                    role = chat_session_item_rs[4]
                )
            )
