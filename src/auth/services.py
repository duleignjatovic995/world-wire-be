import uuid
from datetime import timedelta, datetime
from typing import Optional

import jwt
from fastapi import HTTPException
from jwt import PyJWTError
from passlib.context import CryptContext
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_422_UNPROCESSABLE_ENTITY

from src.auth.consts import TOKEN_TYPE
from src.auth.dtos import UserCredentials, Token, JWTUserDto, SignupDto
from src.common.models import User
from src.common.utils import FlexibleJSONEncoder
from src.settings import settings


class AuthService:
    """
    Class for handling authentication logic
    """

    def __init__(self, db: Session):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def _get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def _build_access_token_data(self, user: User) -> dict:
        return {"sub": user.id}

    def _create_access_token(self, user: User) -> str:
        to_encode = self._build_access_token_data(user)
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.JWT_SIGN_ALGORITHM,
            json_encoder=FlexibleJSONEncoder,
        )
        return encoded_jwt

    def get_user(self, username: str) -> Optional[User]:
        return (
            self.db.query(User)
            .filter(or_(User.username == username, User.email == username))
            .first()
        )

    def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def login_user(self, credentials: UserCredentials) -> Optional[Token]:
        user = self.get_user(credentials.username)

        if not user:
            return None

        if not self._verify_password(credentials.password, user.password):
            return None

        return Token(
            access_token=self._create_access_token(user),
            token_type=TOKEN_TYPE,
        )

    def get_current_user(self, token: str) -> Optional[User]:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.JWT_SIGN_ALGORITHM]
            )
        except PyJWTError:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Basic"},
            )

        user_id: uuid.UUID = payload.get("sub")
        if user_id is None:
            return None

        user = self.get_user_by_id(user_id)
        return user

    def get_current_jwt_user(self, token: str) -> JWTUserDto:
        if token is None:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Basic"},
            )
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.JWT_SIGN_ALGORITHM]
            )
        except PyJWTError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Basic"},
            )

        return JWTUserDto(**payload)

    def signup_user(self, signup_request: SignupDto) -> User:
        user = User(
            username=signup_request.username,
            email=signup_request.email,
        )
        user.password = self._get_password_hash(signup_request.password1)

        try:
            self.db.add(user)
            self.db.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Basic"},
            )

        self.db.add(user)
        self.db.commit()

        return user
