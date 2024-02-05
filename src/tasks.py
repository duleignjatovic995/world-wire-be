from src.celery_config import app
from src.common.db import SessionLocal
from src.countries.ingest.etl_builder import CountryETLBuilder


@app.task
def ingest_countries():
    with SessionLocal() as db:
        etl = CountryETLBuilder(db).set_fetcher().set_processor().set_loader().build()
        etl.run_pipeline()
