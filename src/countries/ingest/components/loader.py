"""
This module stores loading part of country ingestion logic
"""
from abc import ABC

import polars as pl
from sqlalchemy.orm import Session


class BaseCountryLoader(ABC):
    """
    Abstract class for storing countries dataframe.
    To be extended for concrete storage mechanisms.
    """

    def store(self, countries_df: pl.DataFrame):
        pass


class PgCountryLoader(BaseCountryLoader):
    def __init__(self, db: Session):
        self._db = db

    def store(self, countries_df: pl.DataFrame) -> None:
        """
        This method stores Polars DataFrame holding country information
        into relational database.
        :param countries_df: country dataframe
        """
        pass
