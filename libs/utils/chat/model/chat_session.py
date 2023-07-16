class ChatSession:
    id = 0
    iso_created_at = ""
    title = ""
    items = []

    def __init__(self, id = 0, iso_created_at = "", title = "", items = []) -> None:
        self.iso_created_at = iso_created_at
        self.title = title
        self.items = items
