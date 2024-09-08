from models.db import Base
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func


class ChatHistory(Base):
    __tablename__ = "chat_history"
    history_id = Column(String(100), primary_key=True, comment="id")
    user_id = Column(String(100), nullable=False)
    history_name = Column(String(50))
    description = Column(String(255))
    messages = Column(Text)
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now())
