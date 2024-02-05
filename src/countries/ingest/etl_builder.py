from abc import ABC

from sqlalchemy.orm import Session

from src.countries.ingest.components.fetcher import CountryData
from src.countries.ingest.components.loader import PgCountryLoader
from src.countries.ingest.components.processor import DensityCountryProcessor
from src.countries.ingest.etl import CountryETL


class BaseCountryETLFactory(ABC):
    """
    Abstract class for country etl factory
    """

    def create(self) -> CountryETL:
        raise NotImplementedError


class CountryETLFactory(BaseCountryETLFactory):
    """
    Concrete factory for creating ETL executor based
    on separate components
    """

    def __init__(self, db: Session):
        self._db = db

    def create(self) -> CountryETL:
        return CountryETL(
            data=CountryData(),
            processor=DensityCountryProcessor(),
            loader=PgCountryLoader(db=self._db),
        )
