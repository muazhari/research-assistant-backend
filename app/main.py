import logging
from uuid import UUID

import nltk
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseConfig

from app.outers.interfaces.deliveries.routers.api import api_router

logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.DEBUG)

nltk.download('punkt')
nltk.download('cmudict')
nltk.download('averaged_perceptron_tagger')

BaseConfig.json_encoders = {
    UUID: jsonable_encoder,
}

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
