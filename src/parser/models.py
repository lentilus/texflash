from pydantic import BaseModel

class FlashCard(BaseModel):
    question: str
    source: str
