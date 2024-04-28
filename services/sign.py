from datetime import timedelta
from utils.encrypt import create_access_token
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.settings import Setting
from models.answer import ResMsg, HttpCode
from models.user import UserSignUp, UserSignIn
from models.db import UserInfo
from models.token import Token
from passlib.context import CryptContext
from uuid import uuid1

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SignService:
    def __init__(self, db: Session, settings: Setting):
        self.db = db
        self.settings = settings
        self._setting = self.settings.get_settings()

    def sign_up_by_user(self, sign_up_data: UserSignUp) -> ResMsg:
        user = self.db.query(UserInfo).filter(UserInfo.username == sign_up_data.username).first()
        if user:
            return ResMsg(msg="用户已存在", code=HttpCode.HTTP_0_FAIL)
        encrypt_pwd = pwd_context.hash(sign_up_data.password)
        new_user = UserInfo(
            user_id=str(uuid1()),
            username=sign_up_data.username,
            password=encrypt_pwd
        )
        self.db.add(new_user)
        return ResMsg(msg="添加成功！！")

    def sign_in_by_user(self, sign_in_data: UserSignIn) -> Token:
        auth_result = self.authenticate_user(sign_in_data)
        if not auth_result:
            raise HTTPException(
                status_code=HttpCode.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )

        access_token_expires = timedelta(minutes=self._setting.get("authentication", {}).get("expire", 60))
        access_token = create_access_token(
            data={"sub": sign_in_data.username},
            secret_key=self._setting.get("authentication", {}).get("api_key"),
            expires_delta=access_token_expires)
        return Token(access_token=access_token, token_type="bearer")

    def authenticate_user(self, sign_in_data: UserSignIn):
        user: UserInfo = self.db.query(UserInfo).filter(UserInfo.username == sign_in_data.username).first()
        if not user:
            return False
        return pwd_context.verify(sign_in_data.password, user.password)
