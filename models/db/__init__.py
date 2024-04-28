from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from models.db.user import UserInfo, UserProfile


