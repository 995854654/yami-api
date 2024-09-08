from enum import Enum


class CustomStatus(int, Enum):
    AUTH_1001_LOGIN_EXPIRED = 1001  # 用户登录已过期


# website health check
class WebsiteStatus(int, Enum):
    READY = 1
    FAIL = -1
    OTHER = 0
