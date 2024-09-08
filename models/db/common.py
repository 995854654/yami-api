from models.db import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func


# LLM模型表
class LLMModel(Base):
    __tablename__ = "llm_model"
    id = Column(Integer, primary_key=True, comment="id")
    model_id = Column(String(100), nullable=False)
    model_type = Column(String(255), nullable=False)
    model_name = Column(String(255), nullable=False)
    create_time = Column(DateTime, server_default=func.now())


# 功能模块
class FunctionModule(Base):
    __tablename__ = "function_module"
    id = Column(Integer, primary_key=True, comment="id")
    module_id = Column(String(100), nullable=False)
    module_name = Column(String(255), nullable=False)
    create_time = Column(DateTime, server_default=func.now())
