import uuid
from typing import Optional

from pydantic import Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from src.common.dto_config import BaseModel


class UserCredentials(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class SignupDto(BaseModel):
    username: str = Field(..., min_length=6, max_length=100)
    email: str
    password1: str
    password2: str

    @field_validator("password2")
    def passwords_match(cls, v: str, info: ValidationInfo) -> str:
        if "password1" in info.data and v != info.data["password1"]:
            raise ValueError("passwords do not match")
        return v


class JWTUserDto(BaseModel):
    id: uuid.UUID = Field(..., alias="sub")


class UserDto(BaseModel):
    id: uuid.UUID
    email: Optional[str]
    username: Optional[str]
