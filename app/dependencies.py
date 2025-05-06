from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

SECRET_KEY = "OvwHhIjs|)os0LO0bgMh0f>;(k75A4N={s`V&'[u'`OEih)YWd"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.error("Token validation failed: No username in payload")
            raise credentials_exception
    except JWTError as e:
        logger.error(f"Token validation failed: {str(e)}")
        raise credentials_exception
    return User(username=username)