import os
from functools import lru_cache
from pathlib import Path
from utils.logger import LoguruLogger
from models.settings import Setting
from models.token import TokenData
from sqlalchemy.orm import sessionmaker, Session
from services.sign import SignService
from services.chat import ChatService
from services.storage import LocalStorageService
from services.resource import ResourceService
from services.job import JobService
from routes import oauth2_scheme
from fastapi import Depends, HTTPException, Query, status
import jwt
from typing import Optional


@lru_cache
def get_init_settings():
    PROJECT_ROOT_PATH = os.getcwd()
    config_path = Path(PROJECT_ROOT_PATH + "/config/application.yml")
    return Setting(config_path=str(config_path))


def get_db():
    logger = LoguruLogger.get_logger()
    settings: Setting = get_init_settings()
    _session = sessionmaker(bind=settings.metastore)
    session: Session = _session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        logger.info("db操作异常，已回滚!")
        raise
    finally:
        session.close()
        logger.info("db close")


def verify_user_request(token: str = Depends(oauth2_scheme)) -> TokenData:
    setting = get_init_settings().get_settings()
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, setting.get("authentication").get("api_key"), algorithms=["HS256"])
        username: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username, user_id=user_id)
    except Exception as err:
        raise credential_exception
    return token_data


def verify_user_request_for_token(token: Optional[str] = Query(None)):
    logger = LoguruLogger.get_logger()
    setting = get_init_settings().get_settings()
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, setting.get("authentication").get("api_key"), algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username, user_id=payload.get("user_id"))
    except Exception as err:
        logger.error("验证失败：" + str(err))
        raise credential_exception
    return token_data


@lru_cache
def get_storage_service():
    settings = get_init_settings()
    _setting = settings.get_settings()
    storage_type = _setting.get("storage").get("type")
    if storage_type == "local":
        return LocalStorageService(settings=settings)
    else:
        return None


def get_chat_service():
    return ChatService(setting=get_init_settings())


def get_sign_service(db: Session):
    return SignService(db, settings=get_init_settings())


def get_resource_service(db: Session, user_id: str):
    return ResourceService(db=db, user_id=user_id, storage=get_storage_service())


def get_job_service(db: Session, username: str):
    return JobService(db=db, username=username)