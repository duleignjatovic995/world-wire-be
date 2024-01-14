from fastapi import APIRouter

status_router = APIRouter()


@status_router.get("/status")
def get_service_status():
    return {"status": "OK"}
