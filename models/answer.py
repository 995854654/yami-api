from typing import Optional
from pydantic import BaseModel
from models.http import HttpStatus


class ResMsg(BaseModel):
    msg: str = ""
    code: HttpStatus = HttpStatus.SUCCESS
    data: Optional[dict] = None

