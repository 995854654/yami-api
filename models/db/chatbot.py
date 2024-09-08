from models.db import Base
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import datetime


class ChatHistory(Base):
    __tablename__ = "chat_history"
    history_id = Column(String(100), primary_key=True, comment="id")
    user_id = Column(String(100), nullable=False)
    history_name = Column(String(50))
    description = Column(String(255))
    messages = Column(Text)
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now())


class ChatHistoryBase(BaseModel):
    history_id: str
    history_name: str
    description: str
    messages: str
    create_time: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda x: x.strftime("%Y-%m-%d %H:%M:%S")
        }
