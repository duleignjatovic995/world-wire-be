from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from src import tasks
from src.common.api.pagination import PaginationDto
from src.countries.dtos import GetCountryResponseDto
from src.countries.resolvers import get_country_service
from src.countries.services import CountryService

router = APIRouter()


@router.post("/ingest")
def ingest_countries():
    """
    Route for triggering country ingest
    """
    tasks.ingest_countries.delay()


@router.get(
    "/",
    status_code=HTTP_200_OK,
    response_model=GetCountryResponseDto,
)
def get_countries(
    pagination: PaginationDto = Depends(),
    country_service: CountryService = Depends(get_country_service),
):
    """
    Route for getting paginated list of countries
    :param pagination: limit and offset parametes
    :param country_service: country service for fetching list of countries
    :return: list of countries
    """
    return country_service.get_countries(pagination)
