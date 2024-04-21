from pydantic import BaseModel
from typing import Optional


class UserInfo(BaseModel):
    username: str
    email: Optional[str] = None
    disabled: Optional[bool] = None
    full_name: Optional[str] = None
