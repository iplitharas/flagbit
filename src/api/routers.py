from fastapi import FastAPI

from src.api.dependencies import get_flagship_service
from src.domain.flag import Flag
from src.services.flagship import FlagShipService
from pydantic import BaseModel
from fastapi import Depends

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





@app.get(
    "/flags",
    tags=["Flags"],
    name="Get all flags",
    response_model=list[Flag] | None,
    description="Retrieve all feature flags",
)
def flags(
    flagship: FlagShipService = Depends(get_flagship_service),
) -> list[Flag] | None:
    return flagship.get_all_flags()


@app.get(
    "/flags/{flag_name}",
    tags=["Flags"],
    name="Get a flag",
    response_model=Flag,
    description="Retrieve a feature flag by name",
)
def get_flag(flag_name: str, flagship: FlagShipService = Depends(get_flagship_service)) -> Flag:
    return flagship.get_flag_by_name(name=flag_name)


@app.get(
    "/flags/{flag_id}",
    tags=["Flags"],
    response_model=Flag,
    name="Get a flag",
    description="Retrieve a feature flag by ID",
)
def get_flag_by_id(flag_id: str, flagship: FlagShipService = Depends(get_flagship_service)) -> Flag:
    flag = flagship.get_flag_by_id(flag_id=flag_id)
    if not flag:
        raise ValueError("Flag not found")
    return flag


@app.post(
    "/flags",
    tags=["Flags"],
    name="Create a new flag",
    description="Create a new feature flag",
)
def new_flag(flag: FlagRequest) -> bool:
    flagship.create_flag(name=flag.name, value=flag.value)
    return True


@app.patch(
    "/flags/{flag_name}",
    tags=["Flags"],
    name="Update an existing flag",
    description="Update an existing feature flag",
)
def update_flag_by_name(flag_name: str, updated_fields: FlagUpdateRequest, flagship: FlagShipService = Depends(get_flagship_service)) -> Flag:
    existing_flag = flagship.get_flag_by_name(name=flag_name)
    if not existing_flag:
        raise ValueError("Flag not found")
    updated_flag = flagship._update_flag(
        flag_id=str(existing_flag.id),
        updated_fields=updated_fields.model_dump(exclude_unset=True),
    )
    return updated_flag


@app.patch(
    "/flags/{flag_id}",
    tags=["Flags"],
    name="Update an existing flag",
    description="Update an existing feature flag",
)
def update_flag(flag_id: str, updated_fields: FlagUpdateRequest, flagship: FlagShipService = Depends(get_flagship_service)) -> Flag:
    updated_flag = flagship._update_flag(
        flag_id=flag_id, updated_fields=updated_fields.model_dump(exclude_unset=True)
    )
    return updated_flag


@app.delete(
    "/flags/{flag_id}",
    tags=["Flags"],
    name="Delete a flag",
    description="Delete a feature flag by ID",
)
def delete_flag(flag_id: str, flagship: FlagShipService = Depends(get_flagship_service)) -> bool:
    success = flagship.delete_flag_by_id(flag_id=flag_id)
    if not success:
        raise ValueError("Flag not found")
    return success
