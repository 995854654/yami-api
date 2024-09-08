from typing import Optional
from pydantic import BaseModel
from fastapi import status


class ResMsg(BaseModel):
    success: bool = True
    msg: str = "Successfully!!"
    code: int = status.HTTP_200_OK
    data: Optional[object] = None
