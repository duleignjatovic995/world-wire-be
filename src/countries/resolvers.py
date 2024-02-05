from fastapi import Depends
from sqlalchemy.orm import Session

from src.common.resolvers import get_db
from src.countries.services import CountryService


def get_country_service(db: Session = Depends(get_db)):
    return CountryService(db=db)
