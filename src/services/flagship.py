from src.domain.flag import Flag
from src.helpers import new_expiration_date_from_now
from src.types import EXP_UNIT_T


from typing import TypedDict


class FlagAllowedUpdates(TypedDict):
    name: str | None
    value: bool | None
    desc: str | None


class FlagShipRepo:
    def __init__(self) -> None:
        self.store: dict[str, Flag] = {}

    def save(self, flag: Flag) -> Flag:
        self.store[str(flag.id)] = flag
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
        Users can `add` new `Flags` to their `store` by `name` and `value`.
        Optionally, they can provide a `desc` and an expiration date.

        """
        expiration_date = new_expiration_date_from_now(unit=exp_unit, value=exp_value)
        new_flag = Flag(
            name=name, value=value, desc=desc, expiration_date=expiration_date
        )
        self.repo.save(flag=new_flag)
        return new_flag

    def update_flag(self, flag_id: str, updated_fields: FlagAllowedUpdates) -> Flag:
        """
        Users can `update` existing `Flags` in their `store` by `id`.
        """
        existing_flag = self.repo.store.get(flag_id)
        if not existing_flag:
            raise ValueError("Flag not found")

        for key, value in updated_fields.items():
            setattr(existing_flag, key, value)

        self.repo.save(existing_flag)
        return existing_flag

    def list(self) -> list[Flag]:
        print(self.repo.store)
        return list(self.repo.store.values())
