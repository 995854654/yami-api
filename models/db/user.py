from models.db import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from pydantic import BaseModel

class UserInfo(Base):
    __tablename__ = "user_info"
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), unique=True, index=True, comment="用户id")
    username = Column(String(100), unique=True, comment="用户名")
    password = Column(String(255), comment="密码")
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now())




class UserProfile(Base):
    __tablename__ = "user_profile"
    id = Column(Integer, primary_key=True, comment="id")
    user_id = Column(String(100), unique=True, index=True, comment="用户ID")
    name = Column(String(100), comment="用户姓名")
    email = Column(String(255), comment="邮箱")
    avatar_path = Column(String(255), comment="头像地址")
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now())



class UserBase(BaseModel):
    user_id: str
    username: str
    password: str

    class Config:
        from_attributes = True
