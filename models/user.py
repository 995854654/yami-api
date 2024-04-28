from pydantic import BaseModel, validator
from utils.exception import ValidateError


class UserSignUp(BaseModel):
    # 用户注册
    username: str
    password: str

    # 未来可能有其他参数，比如验证码等等

    @validator("username")
    @classmethod
    def strip_username(cls, value):
        if value is None or value == "":
            raise ValidateError("username不能为空")
        return value.strip()


class UserSignIn(BaseModel):
    # 用户登录
    username: str
    password: str
