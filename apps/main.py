from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

from apps.container import application_container
from apps.inners.use_cases.graphs.passage_search_graph import PassageSearchGraph
from apps.outers.interfaces.deliveries.middlewares.authorization_middleware import AuthorizationMiddleware
from apps.outers.interfaces.deliveries.middlewares.session_middleware import SessionMiddleware
from tools import cache_tool


@asynccontextmanager
async def lifespan(app: FastAPI):
    passage_search_graph: PassageSearchGraph = app.container.use_cases.graphs.passage_search()
    cache_tool.set_cache(
        key="embedding_model/BAAI/bge-m3",
        value=passage_search_graph.get_bge_m3_embedding_model(model_name="BAAI/bge-m3")
    )
    cache_tool.set_cache(
        key="reranker_model/BAAI/bge-reranker-v2-m3",
        value=passage_search_graph.get_reranker_model(model_name="BAAI/bge-reranker-v2-m3")
    )
    yield
    cache_tool.delete_cache()


app: FastAPI = FastAPI(
    title="research-assistant-backend",
    version="0.0.2",
    dependencies=[Depends(application_container.routers.security())],
    lifespan=lifespan
)

app.container = application_container

app.add_middleware(
    middleware_class=AuthorizationMiddleware,
    session_management=app.container.use_cases.managements.session(),
)

app.add_middleware(
    middleware_class=SessionMiddleware,
    one_datastore=app.container.datastores.one()
)

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(
    router=application_container.routers.api().router
)
