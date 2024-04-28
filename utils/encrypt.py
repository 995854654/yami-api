import hashlib
import jwt
from datetime import datetime, timedelta, timezone
from typing import Union
from utils.exception import ValidateError


# 前期测试用户注册，后期该函数将会过期
def hash_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()


# 创建token
def create_access_token(data: dict, secret_key, expires_delta: Union[timedelta, None] = None):
    if secret_key is None or secret_key == "":
        raise ValidateError("缺乏secret_key")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encode_jwt


if __name__ == '__main__':
    pwd = "123456"
    # e10adc3949ba59abbe56e057f20f883e
    print(hash_password(pwd))
