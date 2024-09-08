from fastapi import APIRouter, Security, Depends
from models.token import TokenData
from models.custom_request import QARequest, SaveMessageRequest
from services.common import verify_user_request, get_chat_service, get_db
from utils.logger import LoguruLogger
from sse_starlette import EventSourceResponse
from sqlalchemy.orm import Session

chat_router = APIRouter(
    tags=["chat"]
)


@chat_router.post("/chat/qa")
async def qa(request: QARequest, token: TokenData = Security(verify_user_request)):
    logger = LoguruLogger.get_logger()
    logger.info(f"<{token.username}> call qa API, context: {request.context}")
    service = get_chat_service()
    return EventSourceResponse(service.chat_simple_qa(request))


@chat_router.post("/chat/saveMessages")
def save_message(request: SaveMessageRequest, db: Session = Depends(get_db), token: TokenData = Security(verify_user_request)):
    logger = LoguruLogger.get_logger()
    logger.info(f"<{token.username}> call save message API")
    return get_chat_service().update_chat_history(db, request.history_id, request.history_list, token.user_id)


@chat_router.get("/chat/history")
def get_history(db: Session = Depends(get_db), token: TokenData = Security(verify_user_request)):
    logger = LoguruLogger.get_logger()
    logger.info(f"<{token.username}> call get chat history API")
    return get_chat_service().get_chat_history(db, token.user_id)
