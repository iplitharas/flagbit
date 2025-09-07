from src.domain.flag import Flag
from uuid import UUID

from src.helpers import new_expiration_date_from_now
from src.types import EXP_UNIT_T


class FlagShipRepo:
    def __init__(self) -> None:
        self.store: dict[UUID, Flag] = {}

    def save(self, flag: Flag) -> Flag:
        self.store[flag.id] = flag
        return flag


class FlagShipService:
    def __init__(self, repo: FlagShipRepo | None = None) -> None:
        self.repo = repo or FlagShipRepo()

    def add(
        self,
        name: str,
        value: bool,
        desc: str | None = None,
        exp_unit: EXP_UNIT_T = "w",
        exp_value: int = 4,
    ) -> Flag:
        """
        Users can `add` new `Flags` to their `store` by `name` and `value`
        """
        expiration_date = new_expiration_date_from_now(unit=exp_unit, value=exp_value)
        new_flag = Flag(
            name=name, value=value, desc=desc, expiration_date=expiration_date
        )
        self.repo.save(flag=new_flag)
        return new_flag

    def list(self) -> list[Flag]:
        print(self.repo.store)
        return list(self.repo.store.values())
