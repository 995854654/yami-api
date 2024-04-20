import time

import jwt

# 加密算法配置
keys = {
    "alg": "HS256",
    "type": "JWT"
}

salt = "kap02Aj2;x)`(s.="
# 超时时间
exp = int(time.time() + 1)

profile = {
    "username": "Jun Jian Yang",
    "email": "995854654@qq.com",
    "exp": exp
}

token = jwt.encode(payload=profile, key=salt, headers=keys)
print(token)

info = jwt.decode(token, key=salt, verify=True, algorithms="HS256")

time.sleep(3)
print(info)