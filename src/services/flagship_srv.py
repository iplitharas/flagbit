from src.flag import Flag
from uuid import UUID


class FlagShipRepo:
    def __init__(self) -> None:
        self.store: dict[UUID, Flag] = {}

    def save(self, flag: Flag) -> Flag:
        self.store[flag.id] = flag
        return flag


class FlagShipService:
    def __init__(self, repo: FlagShipRepo | None = None) -> None:
        self.repo = repo or FlagShipRepo()

    def add(self, name: str, value: bool, desc: str | None = None) -> Flag:
        """
        Users can `add` new `Flags` to their `store` by `name` and `value`
        """
        new_flag = Flag(name=name, value=value, desc=desc)
        self.repo.save(flag=new_flag)
        return new_flag

    def list(self) -> list[Flag]:
        return list(self.repo.store.values())
