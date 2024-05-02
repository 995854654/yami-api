from fastapi import APIRouter, Depends
from models.user import UserSignUp, UserSignIn
from models.token import Token
from utils.logger import LoguruLogger
from sqlalchemy.orm import Session
from models.answer import ResMsg
from services.common import get_sign_service
from services.common import get_db
from fastapi.security import OAuth2PasswordRequestForm

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


@security_router.post("/login_in")
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    logger = LoguruLogger.get_logger()
    token = get_sign_service(db).sign_in_by_user(
        UserSignIn(username=form_data.username, password=form_data.password)
    )
    logger.info(f"user<{form_data.username}> sign in successfully!")
    return token



