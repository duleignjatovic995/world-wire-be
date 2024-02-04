"""
This module holds all the logic for pre-processing ingested country data
"""
from src.countries.ingest.components.types import RawCountryDTO
import polars as pl


class DensityCountryProcessor:
    """
    This class is a simple population density calculator for
    country data based on area (km2) and population fields.
    """

    @staticmethod
    def process_countries(countries: list[RawCountryDTO]) -> pl.DataFrame:
        """
        Method for calculating population density with Polars
        :param countries:list of country DTOs
        :return: pl.DataFrame
        """
        return (
            pl.DataFrame(countries)
            .lazy()
            .with_columns((pl.col("population") / pl.col("area")).alias("density"))
            .collect()
        )
