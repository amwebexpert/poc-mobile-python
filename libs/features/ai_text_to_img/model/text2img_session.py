from datetime import datetime


class Text2ImgSession:
    id: int
    iso_created_at: str
    query: str
    base64: str
    base64_seed: str

    def __init__(self,  # pylint: disable=too-many-arguments
                 id: int = 0,  # pylint: disable=redefined-builtin, invalid-name
                 iso_created_at: str = None,
                 query: str = None,
                 base64: str = None,
                 base64_seed: str = None,
                 iso_response_received_at: str = None,
                 ) -> None:
        self.id = id  # pylint: disable=redefined-builtin, invalid-name
        self.iso_created_at = iso_created_at
        self.query = query
        self.base64 = base64
        self.base64_seed = base64_seed
        self.iso_response_received_at = iso_response_received_at

        # override None values with defaults
        if self.iso_created_at is None:
            self.iso_created_at = datetime.utcnow().isoformat()

    def __str__(self):
        return f"Text2ImgSession(id={self.id}, title={self.query}, items={self.base64}, iso_created_at={self.iso_created_at})"
