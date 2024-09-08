from models.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from pydantic import BaseModel


class ResourceInfo(Base):
    __tablename__ = "resource_info"
    id = Column(Integer, primary_key=True)
    resource_id = Column(String(100), nullable=False)
    job_id = Column(String(100), nullable=False)
    user_id = Column(String(100), nullable=False)
    resource_name = Column(String(255), comment="资源名称")
    data_source = Column(String(255), comment="来源")
    resource_url = Column(Text, comment="资源路径")
    create_time = Column(DateTime, server_default=func.now())


class ResourceBase(BaseModel):
    resource_id: str
    resource_name: str
    data_source: str

    class Config:
        from_attributes = True
