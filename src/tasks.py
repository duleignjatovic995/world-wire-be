from src.celery_config import app
from src.countries.ingest.etl_builder import CountryETLBuilder


@app.task
def ingest_countries():
    db = None
    etl = CountryETLBuilder(db=db).set_fetcher().set_processor().set_loader().build()
    etl.run_pipeline()
