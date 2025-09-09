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


app = FastAPI(
    title="Feature Flag API",
    version="1.0.0",
    description="API for managing feature flags",
)

flagship = FlagShipService()


@app.get(
    "/flags",
    tags=["Flags"],
    response_model=list[Flag],
    description="Retrieve all feature flags",
)
def flags() -> list[Flag]:
    return flagship.list()

@app.get(
    "/flags/{flag_name}",
    tags=["Flags"],
    response_model=Flag,
    description="Retrieve a feature flag by name",
)
def get_flag(flag_name: str) -> Flag:
    return flagship.get_flag_by_name(name=flag_name)

@app.get("/flags/{flag_id}", tags=["Flags"], response_model=Flag, description="Retrieve a feature flag by ID")
def get_flag_by_id(flag_id: str) -> Flag:
    flag = flagship.get_flag_by_id(flag_id=flag_id)
    if not flag:
        raise ValueError("Flag not found")
    return flag




@app.post("/fags", tags=["Flags"], description="Create a new feature flag")
def new_flag(flag: FlagRequest) -> bool:
    flagship.create_flag(name=flag.name, value=flag.value)
    return True



@app.patch(
    "/flags/{flag_name}", tags=["Flags"], description="Update an existing feature flag"
)
def update_flag_by_name(flag_name: str, updated_fields: FlagUpdateRequest) -> Flag:
    existing_flag = flagship.get_flag_by_name(name=flag_name)
    if not existing_flag:
        raise ValueError("Flag not found")
    updated_flag = flagship._update_flag(
        flag_id=str(existing_flag.id),
        updated_fields=updated_fields.model_dump(exclude_unset=True),
    )
    return updated_flag


@app.patch(
    "/flags/{flag_id}", tags=["Flags"], description="Update an existing feature flag"
)
def update_flag(flag_id: str, updated_fields: FlagUpdateRequest) -> Flag:
    updated_flag = flagship._update_flag(
        flag_id=flag_id, updated_fields=updated_fields.model_dump(exclude_unset=True)
    )
    return updated_flag
