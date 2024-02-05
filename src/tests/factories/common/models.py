import factory

from src.auth.dtos import SignupDto
from src.common.db import SessionLocal

factory_session = SessionLocal()


class SignupDtoFactory(factory.Factory):
    class Meta:
        model = SignupDto

    email = factory.Faker("email")
    username = factory.Faker("name")
    password1 = factory.Faker("password", length=15)
    password2 = factory.SelfAttribute("password1")
