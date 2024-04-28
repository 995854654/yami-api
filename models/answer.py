from typing import Optional
from pydantic import BaseModel
from enum import Enum
# from starlette import status

class HttpCode(int, Enum):
    HTTP_200_OK = 200
    HTTP_0_FAIL = 0
    HTTP_400_BAD_REQUEST = 400
    HTTP_403_FORBIDDEN = 403
    HTTP_404_NOT_FOUND = 404
    HTTP_422_VALIDATE_FAIL = 422
    HTTP_401_UNAUTHORIZED = 401


class ResMsg(BaseModel):
    msg: str = ""
    code: int = HttpCode.HTTP_200_OK
    data: Optional[dict] = None
