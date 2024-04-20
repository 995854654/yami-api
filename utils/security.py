from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
token = Depends(oauth2_scheme)
print(oauth2_scheme)