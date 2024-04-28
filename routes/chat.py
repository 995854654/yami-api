from fastapi import APIRouter, Depends
from models.token import TokenData
from models.answer import ResMsg
from services.common import verify_user_request

chat_router = APIRouter(
    tags=["chat"]
)


@chat_router.get("/chat")
def qa(token: TokenData = Depends(verify_user_request)):
    return ResMsg(msg="验证通过", data=token)
