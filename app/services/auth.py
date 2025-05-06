from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

SECRET_KEY = "OvwHhIjs|)os0LO0bgMh0f>;(k75A4N={s`V&'[u'`OEih)YWd"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        logger.info("AuthService initialized")

    def get_password_hash(self, password: str) -> str:
        hashed = self.pwd_context.hash(password)
        logger.debug("Generated password hash")
        return hashed

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        verified = self.pwd_context.verify(plain_password, hashed_password)
        logger.debug(f"Password verification result: {verified}")
        return verified

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.debug(f"Created access token for user: {data.get('sub')}")
        return encoded_jwt