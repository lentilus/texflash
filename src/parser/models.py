from pydantic import BaseModel

class FlashCard(BaseModel):
    id: str | None
    front: str | None
    back: str
