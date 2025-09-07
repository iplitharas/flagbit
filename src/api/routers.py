from fastapi import FastAPI

from src.domain.flag import Flag
from src.services.flagship import FlagShipService
from pydantic import BaseModel


class FlagRequest(BaseModel):
    name: str
    value: bool


app = FastAPI()

flagship = FlagShipService()


@app.get("/flags")
def flags() -> list[Flag]:
    return flagship.list()


@app.post("/fags")
def new_flag(flag: FlagRequest) -> bool:
    flagship.add(name=flag.name, value=flag.value)
    return True
