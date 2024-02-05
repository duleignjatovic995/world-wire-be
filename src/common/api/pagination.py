from typing import Generic, List, Optional, TypeVar

from pydantic import Field

from src.common.dto_config import BaseModel

T = TypeVar("T")
DEFAULT_PAGE_SIZE = 50


class PaginationDto(BaseModel):
    limit: Optional[int] = Field(DEFAULT_PAGE_SIZE, gt=0, lt=101)
    offset: int = 0


class PaginatedResponse(BaseModel, Generic[T]):
    limit: int
    offset: int
    count: int
    results: List[T]
