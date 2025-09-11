from contextlib import asynccontextmanager

from src.api.flags_router import flags_router
from fastapi import FastAPI
from src.clients.mongo_db_client import MongoDBAsyncClient




@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore
    mongo_client = MongoDBAsyncClient()
    await mongo_client.connect()
    app.state.mongo_client = mongo_client

    yield

    # Shutdown: close MongoDB
    await mongo_client.close()

app = FastAPI(
    title="Feature Flag API",
    version="1.0.0",
    description="API for managing feature flags",
    lifespan=lifespan
)

app.include_router(flags_router, tags=["Flags"])


