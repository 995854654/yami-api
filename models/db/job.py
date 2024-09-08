from models.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum
from sqlalchemy.sql import func
from pydantic import BaseModel
import enum


class JobType(enum.Enum):
    RESOURCE_DOWNLOAD = "resource_download"


class JobStatus(enum.Enum):
    unknown = 0
    processing = 1
    ready = 2
    fail = 3


class BackgroundJob(Base):
    __tablename__ = "background_job"
    id = Column(Integer, primary_key=True)
    job_id = Column(String(100), nullable=False)
    job_type = Column(Enum(JobType), comment="任务类型")
    creator = Column(String(255), comment="创建者")
    description = Column(Text, comment="描述")
    status = Column(Enum(JobStatus), comment="job状态")
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now())


class BackgroundJobBase(BaseModel):
    job_id: str
    job_type: JobType
    creator: str
    status: JobStatus

    class Config:
        from_attributes = True
