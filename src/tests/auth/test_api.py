from pytest_mock import MockFixture
from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient

from src.auth.dtos import SignupDto, UserDto
from src.common.models import User


def test_signup_valid_payload_creates_verified_user(
    signup_dto: SignupDto,
    mocker: MockFixture,
    client: TestClient,
    db: Session,
) -> None:
    # Act
    resp = client.post("/api/auth/v1/signup", data=signup_dto.model_dump_json())

    # Assert
    cu = db.query(User).filter(User.username == signup_dto.username).first()

    assert resp.status_code == status.HTTP_201_CREATED
    response_dto = UserDto(**resp.json())
    dto_from_db = UserDto.model_validate(cu)
    assert cu is not None
    assert response_dto == dto_from_db
