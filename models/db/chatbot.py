from models.db import Base
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func


class ChatHistory(Base):
    __tablename__ = "chat_history"
    history_id = Column(String(100), comment="id")
    user_id = Column(String(100), nullable=False)
    messages = Column(Text)
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now())
