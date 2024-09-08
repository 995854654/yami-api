from datetime import timedelta
from utils.encrypt import create_access_token
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.settings import Setting
from models.custom_response import ResMsg
from models.user import UserSignUp, UserSignIn
from models.db.user import UserInfo, UserBase
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
            return ResMsg(msg="用户已存在", code=status.HTTP_0_FAIL)
        encrypt_pwd = pwd_context.hash(sign_up_data.password)
        new_user = UserInfo(
            user_id=str(uuid1()),
            username=sign_up_data.username,
            password=encrypt_pwd
        )
        self.db.add(new_user)
        return ResMsg(msg="添加成功！！")

    def sign_in_by_user(self, sign_in_data: UserSignIn) -> ResMsg:
        auth_result = self.authenticate_user(sign_in_data)

        if not auth_result["result"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        user_obj: UserBase = auth_result["info"]
        access_token_expires = timedelta(minutes=self._setting.get("authentication", {}).get("expire", 60))
        access_token = create_access_token(
            data={
                "sub": sign_in_data.username,
                "user_id": user_obj.user_id
            },
            secret_key=self._setting.get("authentication", {}).get("api_key"),
            expires_delta=access_token_expires)
        return ResMsg(data=Token(access_token=access_token, token_type="bearer"))

    def authenticate_user(self, sign_in_data: UserSignIn):
        user: UserInfo = self.db.query(UserInfo).filter(UserInfo.username == sign_in_data.username).first()

        if not user:
            result = False
        else:
            result = pwd_context.verify(sign_in_data.password, user.password)
        return {
            "result": result,
            "info": UserBase.from_orm(user)
        }
