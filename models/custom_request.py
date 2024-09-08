from pydantic import BaseModel, Field
from models.llm import LLMConfiguration


class DownloadResourceRequest(BaseModel):
    url: str = Field(..., description="require field")


class QARequest(BaseModel):
    context: str = Field(..., description="chat content")
    config: LLMConfiguration
