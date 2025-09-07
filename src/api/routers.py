from fastapi import FastAPI

from src.flag import Flag
from src.services.flagship_srv import FlagShipService
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
def new_flag(flag: FlagRequest):
    stored_flag = flagship.add(name=flag.name, value=flag.value)
    return stored_flag.id
