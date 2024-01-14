from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from src.status.api import status_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(status_router, prefix="/healthcheck")

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=9500, reload=True)
