from fastapi import APIRouter
from utils.logger import LoguruLogger
from models.custom_response import ResMsg

home_router = APIRouter(
    tags=["home"],
    include_in_schema=True
)


@home_router.get("/")
def root():
    logger = LoguruLogger.get_logger()
    logger.info("Welcome to the yami-api!!!")
    return ResMsg(msg="Welcome to the yami-api!!!")

