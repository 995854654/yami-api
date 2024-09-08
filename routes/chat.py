from fastapi import APIRouter, Security
from models.token import TokenData
from models.custom_request import QARequest
from services.common import verify_user_request, get_chat_service
from utils.logger import LoguruLogger
from sse_starlette import EventSourceResponse

chat_router = APIRouter(
    tags=["chat"]
)


@chat_router.post("/chat/qa")
async def qa(request: QARequest, token: TokenData = Security(verify_user_request)):
    logger = LoguruLogger.get_logger()
    logger.info(f"<{token.username}> call qa API, context: {request.context}")
    service = get_chat_service()
    return EventSourceResponse(service.chat_simple_qa(request.context))



