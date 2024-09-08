from pydantic import BaseModel
from enum import Enum


class ChatDirection(str, Enum):
    LEFT = "left"
    RIGHT = "right"


class ChatMessage(BaseModel):
    key: str
    direction: ChatDirection
    context: str
