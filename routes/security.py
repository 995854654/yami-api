from fastapi import APIRouter, Depends, Security
from models.user import UserSignUp, UserSignIn
from utils.logger import LoguruLogger
from sqlalchemy.orm import Session
from models.custom_response import ResMsg
from services.common import get_sign_service
from services.common import get_db
from fastapi.security import OAuth2PasswordRequestForm
from services.common import verify_user_request
from models.token import TokenData
from models.custom_status import CustomStatus

security_router = APIRouter(
    tags=["security"],
    include_in_schema=True
)


@security_router.post("/sign_up")
def sign_up(user: UserSignUp, db: Session = Depends(get_db)) -> ResMsg:
    logger = LoguruLogger.get_logger()
    answer = get_sign_service(db).sign_up_by_user(user)
    logger.info("user will sign up")
    return answer


@security_router.post("/log_in")
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> ResMsg:
    logger = LoguruLogger.get_logger()
    answer = get_sign_service(db).sign_in_by_user(
        UserSignIn(username=form_data.username, password=form_data.password)
    )
    logger.info(f"user<{form_data.username}> sign in successfully!")
    return answer


@security_router.get("/refresh_token")
def refresh_token(token: TokenData = Security(verify_user_request)):
    if token.username:
        return ResMsg()
    else:
        return ResMsg(
            success=False,
            code=CustomStatus.AUTH_1001_LOGIN_EXPIRED,
            msg="用户登录已过期，请重新登录"
        )
