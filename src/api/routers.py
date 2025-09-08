from fastapi import FastAPI

from src.domain.flag import Flag
from src.services.flagship import FlagShipService
from pydantic import BaseModel


class FlagRequest(BaseModel):
    name: str
    value: bool


class FlagUpdateRequest(BaseModel):
    name: str | None = None
    value: bool | None = None
    desc: str | None = None


app = FastAPI(title="Feature Flag API", version="1.0.0", description="API for managing feature flags")

flagship = FlagShipService()


@app.get("/flags", tags=["Flags"], response_model=list[Flag], description="Retrieve all feature flags")
def flags() -> list[Flag]:
    return flagship.list()


@app.post("/fags", tags=["Flags"], description="Create a new feature flag")
def new_flag(flag: FlagRequest) -> bool:
    flagship.add(name=flag.name, value=flag.value)
    return True


@app.patch("/flags/{flag_id}", tags=["Flags"], description="Update an existing feature flag")
def update_flag(flag_id: str, updated_fields: FlagUpdateRequest) -> Flag:
    updated_flag = flagship.update_flag(
        flag_id=flag_id, updated_fields=updated_fields.model_dump(exclude_unset=True)
    )
    return updated_flag
