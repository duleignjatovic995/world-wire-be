from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

from src.auth.dtos import UserDto, SignupDto, Token, UserCredentials
from src.auth.resolvers import get_auth_service, get_user_credentials, get_current_user
from src.auth.services import AuthService

router = APIRouter()


@router.post("/signup", response_model=UserDto, status_code=HTTP_201_CREATED)
def signup(
    signup_request: SignupDto,
    auth_service: AuthService = Depends(get_auth_service),
):
    user = auth_service.signup_user(signup_request)
    return UserDto.model_validate(user)


@router.post("/login", response_model=Token)
def login(
    credentials: UserCredentials = Depends(get_user_credentials),
    auth_service: AuthService = Depends(get_auth_service),
):
    token_dto = auth_service.login_user(credentials)
    if not token_dto:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return token_dto


@router.get("/users/me", response_model=UserDto)
def get_current_user(user: UserDto = Depends(get_current_user)):
    return user
