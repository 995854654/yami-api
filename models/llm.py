from pydantic import BaseModel, Field
from enum import Enum

common_description = "One of the large language model parameter"


class LLMType(str, Enum):
    MOONSHOT = "moonshot"
    GPT4TURBO = "gpt-4-turbo"


class LLMConfiguration(BaseModel):
    """
    temperature: 温度。 控制模型输出结果的随机性， 范围：0~1， 值越小，结果的随机性越低， 但不能绝对地控制没有随机性
    top_p：范围：0~1， 具体含义请参考官网。
    frequency_penalty： 频率惩罚，范围：-2~2， 具体含义请参考官网。
    presence_penalty： 存在惩罚， 范围：-2~2， 具体含义请参考官网。
    seed: 随机种子，需要查看模型是否支持该参数
    """
    llm_model_name: str = Field(..., description="One of the large language model name")
    endpoint: str = Field(..., description="Model name endpoint")
    temperature: int = Field(default=0, description=common_description)
    top_p: int = Field(default=1, description=common_description)
    frequency_penalty: int = Field(default=0, description=common_description)
    presence_penalty: int = Field(default=0, description=common_description)
    seed: int = Field(default=255, description=common_description)
