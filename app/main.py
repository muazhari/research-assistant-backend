from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.outer.interfaces.deliveries.routers.api import api_router

app = FastAPI(
    title="research-assistant-backend",
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
