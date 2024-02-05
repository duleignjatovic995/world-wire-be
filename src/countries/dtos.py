from src.common.api.pagination import PaginatedResponse
from src.common.dto_config import BaseModel


class CountryDTO(BaseModel):
    name: str
    alpha2_code: str
    alpha3_code: str
    region: str
    subregion: str
    maps: str
    flag: str
    is_landlocked: bool
    area: float
    population: int
    density: float


class GetCountryResponseDto(PaginatedResponse[CountryDTO]):
    ...
