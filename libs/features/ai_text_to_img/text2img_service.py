from typing import List

from libs.services.storage_service import StorageService
from libs.features.ai_text_to_img.model.text2img_session import Text2ImgSession

class Text2ImgService:
    def __init__(self) -> None:
        self.storage_service = StorageService("text2img_sessions.db")
        self.storage_service.connect()
        self.create_text2img_table()
        self.storage_service.close()
    
    def create_text2img_table(self) -> None:
        self.storage_service.create_table(
            table_name = "text_2_images", 
            columns=(
                "id                        INTEGER PRIMARY KEY AUTOINCREMENT",
                "iso_created_at            TEXT NOT NULL",
                "query                     TEXT NOT NULL",
                "base64                    TEXT NOT NULL",
                "base64_seed               TEXT NOT NULL",
                "iso_response_received_at  TEXT NOT NULL",
            )
        )
    
    def get_all_sessions(self) -> List[Text2ImgSession]:
        self.storage_service.connect()
        result = self.storage_service.select("text_2_images", ["*"])
        elements = []
        for text2img_rs in result:
            text2Img = self.build_from_resultset(text2img_rs)
            elements.append(text2Img)
        self.storage_service.close()
        elements.sort(key=lambda session: session.iso_created_at, reverse=True)
        return elements

    def save(self, text2img_session: Text2ImgSession) -> Text2ImgSession:
        self.storage_service.connect()
        text2img_session.id = self.create(text2img_session)
        self.storage_service.close()
        return text2img_session

    def create(self, text2Img: Text2ImgSession) -> int:
        text2Img.id = self.storage_service.insert(
            table_name="text_2_images", 
            columns=("iso_created_at", "query", "base64", "base64_seed", "iso_response_received_at"),
            values=(text2Img.iso_created_at, text2Img.query, text2Img.base64, text2Img.base64_seed, text2Img.iso_response_received_at)
        )
        return text2Img.id

    def get(self, id = 0) -> Text2ImgSession:
        self.storage_service.connect()
        result = self.storage_service.select("text_2_images", ["*"], f"id = {id}")
        if len(result) == 0:
            return None

        text2img_rs = result[0]
        text2Img = self.build_from_resultset(text2img_rs)
        self.storage_service.close()
        return text2Img

    def build_from_resultset(self, text2img_rs: list[any]) -> Text2ImgSession:
        return Text2ImgSession(
            id = text2img_rs[0], 
            iso_created_at = text2img_rs[1],
            query = text2img_rs[2],
            base64 = text2img_rs[3], 
            base64_seed = text2img_rs[4],
            iso_response_received_at = text2img_rs[5]
        )
