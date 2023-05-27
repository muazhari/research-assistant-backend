from uuid import UUID

import nltk
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseConfig

from app.outers.interfaces.deliveries.routers.api import api_router

nltk.download('punkt')

BaseConfig.json_encoders = {UUID: jsonable_encoder}

app = FastAPI(
    title="research-assistant-backend",
    version="0.0.1"
)

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router=api_router
)
