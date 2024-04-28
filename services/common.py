import os
from functools import lru_cache
from pathlib import Path
from utils.logger import LoguruLogger
from models.settings import Setting
from models.answer import HttpCode
from models.token import TokenData
from sqlalchemy.orm import sessionmaker, Session
from services.sign import SignService
from routes import oauth2_scheme
from fastapi import Depends,HTTPException
import jwt

@lru_cache
def get_init_settings():
    PROJECT_ROOT_PATH = os.getcwd()
    config_path = Path(PROJECT_ROOT_PATH + "/config/application.yml")
    return Setting(config_path=str(config_path))


def get_db():
    logger = LoguruLogger.get_logger()
    settings: Setting = get_init_settings()
    _session = sessionmaker(bind=settings.metastore)
    session = _session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        logger.info("db操作异常，已回滚!")
        raise
    finally:
        session.close()


@lru_cache
def get_sign_service(db: Session):
    return SignService(db, settings=get_init_settings())


def verify_user_request(token: str = Depends(oauth2_scheme)) -> TokenData:
    setting = get_init_settings().get_settings()
    credential_exception = HTTPException(
        status_code=HttpCode.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, setting.get("authentication").get("api_key"), algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except Exception as err:
        raise credential_exception
    return token_data
