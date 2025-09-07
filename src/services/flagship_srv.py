from src.flag import Flag
from uuid import UUID


class FlagShipRepo:
    def store(self):
        pass


class FlagShipService:
    def __init__(self, repo) -> None:
        pass

    def add(self, name: str, value: bool, desc: str | None = None) -> UUID:
        new_flag = Flag(name=name, value=value, desc=desc)
        return new_flag.id
