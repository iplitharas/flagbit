from pydantic import BaseModel


class FlagRequest(BaseModel):
    name: str
    value: bool
    desc: str | None = None


class FlagUpdateRequest(BaseModel):
    name: str | None = None
    value: bool | None = None
    desc: str | None = None
