import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.common.db import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(100), nullable=False, index=True)
    alpha2_code = Column(String(2), nullable=False)
    alpha3_code = Column(String(3), nullable=False)
    region = Column(String(100), nullable=False)
    subregion = Column(String(100), nullable=False)
    maps = Column(String(100), nullable=False)
    flag = Column(String(100), nullable=False)
    is_landlocked = Column(Boolean, default=False)
    area = Column(Numeric, nullable=False)
    population = Column(Numeric, nullable=False)
    density = Column(Numeric, nullable=False)


class AuditModelMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class User(Base, AuditModelMixin):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(200), nullable=True, unique=True, index=True)
    username = Column(String(100), nullable=True, unique=True, index=True)
    password = Column(String, nullable=True)

    refresh_tokens = relationship(
        "RefreshToken", back_populates="user", cascade="all, delete"
    )


class RefreshToken(Base, AuditModelMixin):
    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    value = Column(String(128), nullable=False, unique=True, index=True)
    expires_at = Column(DateTime, nullable=True, index=True)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", back_populates="refresh_tokens")


class CountryBookmark(Base, AuditModelMixin):
    __tablename__ = "country_bookmarks"
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    country_id = Column(
        UUID(as_uuid=True),
        ForeignKey("countries.id", ondelete="CASCADE"),
        primary_key=True,
    )
