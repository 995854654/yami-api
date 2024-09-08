from pydantic import BaseModel, Field
from enum import Enum


class LLMType(str, Enum):
    MOONSHOT = "moonshot"
    GPT4TURBO = "gpt-4-turbo"


class LLMConfiguration(BaseModel):
    llm_model_name: str = Field(...)
    endpoint: str = Field(...)

    max_tokens: int = 2500
    temperature: int = 0
    top_p: int = 1
    top_k: int = 1
    seed: int = 256
    frequency_penalty: int = 0
    presence_penalty: int = 0
