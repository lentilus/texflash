from pydantic import BaseModel

class FlashCard(BaseModel):
    id: str | None
    front: str
    back: str
