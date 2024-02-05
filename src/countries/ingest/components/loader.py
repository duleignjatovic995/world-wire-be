"""
This module stores loading part of country ingestion logic
"""
import logging
from abc import ABC

import polars as pl
from sqlalchemy.orm import Session

from src.common.models import Country


class BaseCountryLoader(ABC):
    """
    Abstract class for storing countries dataframe.
    To be extended for concrete storage mechanisms.
    """

    def store(self, countries_df: pl.DataFrame):
        raise NotImplementedError


class PgCountryLoader(BaseCountryLoader):
    def __init__(self, db: Session):
        self._db = db

    def store(self, countries_df: pl.DataFrame) -> None:
        """
        This method stores Polars DataFrame holding country information
        into relational database.
        :param countries_df: country dataframe
        """

        objs = [Country(**c) for c in countries_df.to_dicts()]
        logging.warning(f"Storing {len(objs)} countries!")
        self._db.bulk_save_objects(objects=objs)
        logging.info("Country ingest successful")
