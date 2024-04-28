from models.db import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func


class AttachmentInfo(Base):
    __tablename__ = "attachment_info"
    id = Column(Integer, primary_key=True, comment="id")
    attachment_id = Column(String(100), nullable=False)
    user_id = Column(String(100), nullable=False, unique=True, index=True)
    filename = Column(String(255), comment="文件名称")
    filetype = Column(String(25), comment="文件类型")
    filesize = Column(String(255), comment="文件大小，中文解释")
    filesize_format = Column(String(255), comment="文件大小，按照标准的大小格式输出")
    filepath = Column(String(255), comment="文件路径")
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now())
