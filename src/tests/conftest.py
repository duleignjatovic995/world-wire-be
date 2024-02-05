from typing import Generator

import pytest
from starlette.testclient import TestClient

from src.auth.dtos import SignupDto
from src.common.db import SessionLocal
from src.main import app
from src.tests.factories.common.models import SignupDtoFactory


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def signup_dto() -> SignupDto:
    return SignupDtoFactory()
