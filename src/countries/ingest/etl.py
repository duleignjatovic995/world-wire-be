"""
This module holds logic for orchestrating extraction transforming and loading of
country data
"""
from src.countries.ingest.components.fetcher import BaseCountryData
from src.countries.ingest.components.loader import BaseCountryLoader
from src.countries.ingest.components.processor import DensityCountryProcessor


class CountryETL:
    def __init__(
        self,
        data: BaseCountryData,
        processor: DensityCountryProcessor,
        loader: BaseCountryLoader,
    ):
        self._data = data
        self._processor = processor
        self._loader = loader

    def run_pipeline(self) -> None:
        """
        Method for orchestrating data ingestion
        """
        processed_countries_df = self._processor.process_countries(
            countries=self._data.countries
        )
        self._loader.store(countries_df=processed_countries_df)
