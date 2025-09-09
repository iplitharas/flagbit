from src.api.flags_router import flags_router
from fastapi import FastAPI


app = FastAPI(
    title="Feature Flag API",
    version="1.0.0",
    description="API for managing feature flags",
)


app.include_router(flags_router, tags=["Flags"])
