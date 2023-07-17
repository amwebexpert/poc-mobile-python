from datetime import datetime

class ChatSession:
    id = 0
    iso_created_at = ""
    title = ""
    items = []

    def __init__(self, id = 0, iso_created_at = datetime.utcnow().isoformat(), title = "", items = []) -> None:
        self.id = id
        self.iso_created_at = iso_created_at
        self.title = title
        self.items = items
