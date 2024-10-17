from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_token(token: str = Depends(oauth2_scheme)):
    if token != os.environ.get("API_SECRET_TOKEN", "secret-token"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token
