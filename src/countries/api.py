from fastapi import APIRouter

from src import tasks

router = APIRouter()


@router.post("/ingest")
def ingest_countries():
    tasks.ingest_countries.delay()
