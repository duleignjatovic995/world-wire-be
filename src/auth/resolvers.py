from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.auth.dtos import UserDto, UserCredentials, JWTUserDto
from src.auth.services import AuthService
from src.common.resolvers import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/v1/login", auto_error=False)


async def get_auth_service(
    db: Session = Depends(get_db),
):
    return AuthService(db=db)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> Optional[UserDto]:
    user = auth_service.get_current_user(token)
    if user is None:
        return None

    return UserDto.model_validate(user)


async def get_current_jwt_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> Optional[JWTUserDto]:
    jwt_user = auth_service.get_current_jwt_user(token)
    if jwt_user is None:
        return None

    return jwt_user


async def get_user_credentials(form_data: OAuth2PasswordRequestForm = Depends()):
    val = {"username": form_data.username, "password": form_data.password}
    return UserCredentials(**val)
