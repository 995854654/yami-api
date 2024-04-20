from fastapi import APIRouter, Depends
from utils.logger import LoguruLogger
from models.answer import ResMsg

from fastapi.security import OAuth2PasswordBearer

home_router = APIRouter(
    tags=["home"],
    include_in_schema=True
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@home_router.get("/")
def root():
    logger = LoguruLogger.get_logger()
    logger.info("Welcome to the yami-api!!!")
    return ResMsg(msg="Welcome to the yami-api!!!")


@home_router.get("/token")
def security(token=Depends(oauth2_scheme)):
    logger = LoguruLogger.get_logger()
    logger.info(token)
    return {"token": token}
