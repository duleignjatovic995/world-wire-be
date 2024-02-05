import uuid

from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src import tasks
from src.auth.dtos import JWTUserDto
from src.auth.resolvers import get_current_jwt_user
from src.common.api.pagination import PaginationDto
from src.countries.dtos import GetCountryResponseDto, CountryDTO
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
    Endpoint for getting paginated list of countries
    :param pagination: limit and offset parametes
    :param country_service: country service for fetching list of countries
    :return: list of countries
    """
    return country_service.get_countries(pagination)


@router.post(
    "/my/countries/{country_id}",
    status_code=HTTP_201_CREATED,
    response_model=CountryDTO,
)
def bookmark_country(
    country_id: uuid.UUID,
    user: JWTUserDto = Depends(get_current_jwt_user),
    country_service: CountryService = Depends(get_country_service),
):
    """
    Endpoint for bookmarking country

    :param country_id: Country ID (can be obtained from "get countries" endpoint)
    :param user: currently logged in used
    :param country_service: country service
    :return:
    """
    raise NotImplementedError


@router.get(
    "/my/countries", status_code=HTTP_201_CREATED, response_model=GetCountryResponseDto
)
def list_bookmarks(
    user: JWTUserDto = Depends(get_current_jwt_user),
    country_service: CountryService = Depends(get_country_service),
):
    """
    Endpoint for listing bookmarked countries
    :param user: currently logged in used
    :param country_service: country service
    :return:
    """
    raise NotImplementedError


@router.delete("/my/countries/{country_id}", status_code=HTTP_204_NO_CONTENT)
def remove_bookmark(
    country_id: uuid.UUID,
    user: JWTUserDto = Depends(get_current_jwt_user),
    country_service: CountryService = Depends(get_country_service),
):
    """
    Endpoint for removing the country from bookmarks.

    :param country_id: Country ID (can be obtained from "get countries" endpoint)
    :param user: currently logged in used
    :param country_service: country service:
    """
    raise NotImplementedError
