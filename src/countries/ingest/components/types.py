from typing import TypedDict


class RawCountryDTO(TypedDict):
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
