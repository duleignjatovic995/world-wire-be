"""
Module for country related API logic
"""
from sqlalchemy.orm import Session

from src.common.api.pagination import PaginationDto
from src.common.models import Country
from src.countries.dtos import CountryDTO, GetCountryResponseDto


class CountryService:
    """
    Class for country related CRUD handling
    """

    def __init__(self, db: Session):
        self.db = db

    def get_countries(self, pagination: PaginationDto) -> GetCountryResponseDto:
        q = self.db.query(Country)

        paginated = q.offset(pagination.offset).limit(pagination.limit)

        result = paginated.all()

        parsed_result = [CountryDTO.model_validate(country) for country in result]
        return GetCountryResponseDto(
            limit=pagination.limit,
            offset=pagination.offset,
            count=q.count(),
            results=parsed_result,
        )

    # todo impement country bookmark
