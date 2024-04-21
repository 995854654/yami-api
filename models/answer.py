from typing import Optional
from pydantic import BaseModel
from fastapi import status

class ResMsg(BaseModel):
    msg: str = ""
    code: int = status.HTTP_200_OK
    data: Optional[dict] = None

