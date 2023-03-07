import time
from jose import JWTError, jwt

from project.config import ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from project.schemas.schemas import TokenResponse


def create_access_token(data: dict) -> TokenResponse:
    to_encode = data.copy()
    expire = time.time() + int(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expiry": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return TokenResponse(token=token)


def decode_token(token: TokenResponse):
    try:
        decoded_token = jwt.decode(token.token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token['email'] if decoded_token['expiry'] >= time.time() else None
    except:
        return None
