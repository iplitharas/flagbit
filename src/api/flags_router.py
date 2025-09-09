from fastapi import APIRouter
from typing import cast
from src.api.dependencies import get_flagship_service
from src.api.models import FlagUpdateRequest, FlagRequest
from src.domain.flag import Flag
from src.services.flagship import FlagShipService, FlagAllowedUpdates
from fastapi import Depends
from fastapi import HTTPException


flags_router = APIRouter()


@flags_router.get(
    "/flags",
    tags=["Flags"],
    name="Get all flags",
    response_model=list[Flag] | None,
    description="Retrieve all feature flags",
)
def flags(
    flagship: FlagShipService = Depends(get_flagship_service),
    flag_name: str | None = None,
) -> list[Flag] | None:
    return flagship.get_all_flags(flag_name=flag_name)


@flags_router.get(
    "/flags/{flag_name}/value",
    tags=["Flags"],
    name="Get flag value",
    description="Retrieve the value of a feature flag by name",
)
def get_flag_value(
    flag_name: str, flagship: FlagShipService = Depends(get_flagship_service)
) -> bool:
    try:
        return flagship.get_flag_value(name=flag_name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@flags_router.get(
    "/flags/{flag_id}",
    tags=["Flags"],
    response_model=Flag,
    name="Get a flag",
    description="Retrieve a feature flag by ID",
)
def get_flag_by_id(
    flag_id: str, flagship: FlagShipService = Depends(get_flagship_service)
) -> Flag:
    if flag := flagship.get_flag(flag_id=flag_id):
        return flag
    raise HTTPException(status_code=404, detail="Flag not found")


@flags_router.post(
    "/flags",
    tags=["Flags"],
    name="Create a new flag",
    description="Create a new feature flag",
    status_code=201,
)
def new_flag(
    flag: FlagRequest, flagship: FlagShipService = Depends(get_flagship_service)
) -> Flag:
    new_flag = flagship.create_flag(name=flag.name, value=flag.value, desc=flag.desc)
    return new_flag


@flags_router.patch(
    "/flags/{flag_id}",
    tags=["Flags"],
    name="Update an existing flag",
    description="Update an existing feature flag",
)
def update_flag(
    flag_id: str,
    updated_fields: FlagUpdateRequest,
    flagship: FlagShipService = Depends(get_flagship_service),
) -> Flag:
    try:
        return flagship.update_flag(
            flag_id=flag_id,
            updated_fields=cast(
                FlagAllowedUpdates, updated_fields.model_dump(exclude_unset=True)
            ),
        )
    except Exception:
        raise HTTPException(status_code=404, detail="Flag not found")


@flags_router.delete(
    "/flags/{flag_id}",
    tags=["Flags"],
    name="Delete a flag",
    description="Delete a feature flag by ID",
)
def delete_flag(
    flag_id: str, flagship: FlagShipService = Depends(get_flagship_service)
) -> bool:
    success = flagship.delete_flag(flag_id=flag_id)
    if not success:
        raise ValueError("Flag not found")
    return success
