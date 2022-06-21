from datetime import datetime, timedelta
from typing import List, MutableMapping, Optional, Union

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from ormar import NoMatch

from app.core.config import settings
from app.core.security import verify_password
from app.models.users import User
from app.schemas.users import UserSignIn

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_VERSION}/auth/token")

JWTPayloadMapping = MutableMapping[str, Union[datetime, bool, str, List[str], List[int]]]


async def authenticate(user_logging_in: UserSignIn) -> Optional[User]:
    try:
        user = await User.objects.get(email=user_logging_in.email)
    except NoMatch:
        return None
    if not verify_password(user_logging_in.password, user.hashed_password):
        return None
    return user


def create_access_token(*, sub: str) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def _create_token(
    token_type: str,
    lifetime: timedelta,
    sub: str,
) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
