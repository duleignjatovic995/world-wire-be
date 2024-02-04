"""
This module holds all country data fetching logic from external providers
"""
from abc import ABC

import requests

from src.countries.ingest.components.types import RawCountryDTO
from src.settings import settings


def parse_country(raw_country: dict) -> RawCountryDTO:
    country_model = {
        "name": raw_country["name"]["common"],
        "alpha2_code": raw_country["cca2"],
        "alpha3_code": raw_country["cca3"],
        "region": raw_country["region"],
        "subregion": raw_country.get("subregion", raw_country["region"]),
        "map": raw_country["maps"]["googleMaps"],
        "flag": raw_country["flags"]["png"],
        "is_landlocked": raw_country["landlocked"],
        "area": raw_country["area"],  # km2
        "population": raw_country["population"],
    }
    return country_model


class BaseCountryData(ABC):
    """
    Abstract class for fetching country data from
    the external provider. To be extended for different data
    providers.
    """

    @property
    def countries(self) -> list[RawCountryDTO]:
        """
        Abstract property for holding collection to the countries to be stored.
        :return:
        """
        raise NotImplementedError


class CountryData(BaseCountryData):
    """
    Class for fetching country data from restcountries.com
    """

    def __init__(self):
        self._countries: list[RawCountryDTO] = []

    @property
    def countries(self) -> list[RawCountryDTO]:
        """
        Property for holding list of country data
        :return: list of countries
        """
        if not self._countries:
            self._countries = self._get_raw_countries()
        return self._countries

    def _get_raw_countries(self):
        countries_response = requests.get(settings.COUNTRY_API_URL).json()
        parsed_countries = [
            parse_country(raw_country)
            for raw_country in countries_response
            if raw_country.get("independent", False)
        ]
        return parsed_countries
