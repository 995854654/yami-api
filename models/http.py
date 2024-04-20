from enum import Enum


class HttpStatus(int, Enum):
    NOT_FUND = 404
    FORBIDDEN = 403
    SUCCESS = 200
    FAIL = -1
    SERVER_ERROR = 500


if __name__ == '__main__':
    print(404 == HttpStatus.NOT_FUND)