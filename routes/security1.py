from jose import JWTError, jwt
from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Union, List
from datetime import datetime, timedelta, timezone
from utils.logger import LoguruLogger

security_router = APIRouter(
    tags=["security"],
    include_in_schema=True
)

SECRET_KEY = "3aa8e412cedeefe2cab00538284c10e8fc4edee454a9c0a3a5ab072bdef5f309"
ALGORITHM = "HS256"  # 算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 过期时间，30min后过期

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        # 这里有多个密码都是可以验证通过的，原因是因为passlib使用了salt随机生成的一个密文。
        # "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "hashed_password": "$2b$12$revuRgGRZ3z5KI0mR6D5KO3n7sauh6aXqS2mMa85AgvQ2ILS020lm",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Chains",
        "email": "alicechains@example.com",
        "hashed_password": "$2b$12$gSvqqUPvlXP2tfVFaWK1Be7DlH.PKZbv5H8KnzzVgXXbVxpva.pFm",
        "disabled": True,
    },
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
    scopes: List[str] = []


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)


# 校验密码
def verify_password(plain_password, hashed_password):
    """

    :param plain_password: 用户输入的未加密密码
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


# 密码加密
def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    logger = LoguruLogger.get_logger()
    logger.info(security_scopes.scope_str)
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except JWTError:
        raise credential_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credential_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


def get_current_active_user(current_user: User = Security(get_current_user, scopes=["me"])):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@security_router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # 为了简明起见，本例把接收的作用域直接添加到了令牌里。

    # 但在您的应用中，为了安全，应该只把作用域添加到确实需要作用域的用户，或预定义的用户。
    access_token = create_access_token(data={"sub": user.username, "scopes": form_data.scopes}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")


@security_router.get("/users/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@security_router.get("/users/me/items")
def read_own_items(current_user: User = Security(get_current_active_user, scopes=["items"])):
    return [{"item_id": "Foo", "owner": current_user.username}]


@security_router.get("/status/")
def read_system_status(current_user: User = Depends(get_current_user)):
    return {"status": "ok"}


if __name__ == '__main__':
    # "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
    # "hashed_password": "$2b$12$revuRgGRZ3z5KI0mR6D5KO3n7sauh6aXqS2mMa85AgvQ2ILS020lm",
    pwd1 = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
    pwd2 = "$2b$12$revuRgGRZ3z5KI0mR6D5KO3n7sauh6aXqS2mMa85AgvQ2ILS020lm"
    pwd = get_password_hash("secret")
    print(pwd)
    print(verify_password("secret", pwd2))
