from abc import ABC
from typing import Optional

from src.countries.ingest.components.fetcher import BaseCountryData, CountryData
from src.countries.ingest.components.loader import BaseCountryLoader, PgCountryLoader
from src.countries.ingest.components.processor import DensityCountryProcessor
from src.countries.ingest.etl import CountryETL


class BaseCountryETLBuilder(ABC):
    def set_fetcher(self):
        raise NotImplementedError

    def set_processor(self):
        raise NotImplementedError

    def set_loader(self):
        raise NotImplementedError

    def build(self) -> CountryETL:
        raise NotImplementedError


class CountryETLBuilder(BaseCountryETLBuilder):
    def __init__(self, db):
        self._db = db

        self._fetcher: Optional[BaseCountryData] = None
        self._processor: Optional[DensityCountryProcessor] = None
        self._loader: Optional[BaseCountryLoader] = None

    def set_fetcher(self):
        if self._fetcher is None:
            self._fetcher = CountryData()
        return self

    def set_processor(self):
        if self._processor is None:
            self._processor = DensityCountryProcessor()
        return self

    def set_loader(self):
        if self._loader is None:
            self._loader = PgCountryLoader(db=self._db)
        return self

    def build(self) -> CountryETL:
        return CountryETL(
            data=self._fetcher, processor=self._processor, loader=self._loader
        )
