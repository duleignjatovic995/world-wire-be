from src.celery_config import app
from src.common.db import SessionLocal
from src.countries.ingest.etl_builder import CountryETLFactory


@app.task
def ingest_countries():
    with SessionLocal() as db:
        etl = CountryETLFactory(db).create()
        etl.run_pipeline()
