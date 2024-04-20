import os
from functools import lru_cache
from pathlib import Path
from utils.logger import LoguruLogger
from models.settings import Settings
from sqlalchemy.orm import sessionmaker


@lru_cache
def get_init_settings():
    PROJECT_ROOT_PATH = os.getcwd()
    logger = LoguruLogger.get_logger()
    logger.info(PROJECT_ROOT_PATH)
    config_path = Path(PROJECT_ROOT_PATH + "/config/application.yml")
    return Settings(config_path=config_path)


def get_db():
    settings: Settings = get_init_settings()
    _session = sessionmaker(bind=settings.metastore)
    session = _session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
