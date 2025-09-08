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


app = FastAPI()

flagship = FlagShipService()


@app.get("/flags")
def flags() -> list[Flag]:
    return flagship.list()


@app.post("/fags")
def new_flag(flag: FlagRequest) -> bool:
    flagship.add(name=flag.name, value=flag.value)
    return True


@app.patch("/flags/{flag_id}")
def update_flag(flag_id: str, updated_fields: FlagUpdateRequest) -> Flag:
    updated_flag = flagship.update_flag(
        flag_id=flag_id, updated_fields=updated_fields.model_dump(exclude_unset=True)
    )
    return updated_flag
