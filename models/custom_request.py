from pydantic import BaseModel, Field
from models.llm import LLMConfiguration
from models.common import ChatMessage
from typing import List


class DownloadResourceRequest(BaseModel):
    url: str = Field(..., description="require field")


class QARequest(BaseModel):
    context: str = Field(..., description="chat content")
    history_id: str = Field(..., alias="historyID")
    history_list: List[ChatMessage] = Field(default=[], alias="messages")
    config: LLMConfiguration = None


class SaveMessageRequest(BaseModel):
    history_id: str = Field(..., alias="historyID")
    history_list: List[ChatMessage] = Field(default=[], alias="messages")
