from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from src.common.migration_utils import execute_migrations
from src.status.api import status_router
from src.countries.api import router as countries_router
from src.auth.api import router as auth_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def migrate():
    execute_migrations()


app.include_router(status_router, prefix="/healthcheck")
app.include_router(countries_router, prefix="/api/v1/countries")
app.include_router(auth_router, prefix="/api/auth/v1")

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=9500, reload=True)
