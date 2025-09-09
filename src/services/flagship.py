from src.domain.flag import Flag
from src.helpers import new_expiration_date_from_now
from src.types import EXP_UNIT_T
from src.exceptions import FlagNotFoundException
from typing import TypedDict


class FlagAllowedUpdates(TypedDict, total=False):
    name: str | None
    value: bool | None
    desc: str | None


class FlagShipRepo:
    def __init__(self) -> None:
        self.store: dict[str, Flag] = {}

    def save(self, flag: Flag) -> Flag:
        self.store[str(flag.id)] = flag
        return flag

    def get_flag_by_name(self, name: str) -> Flag | None:
        for flag in self.store.values():
            if flag.name == name:
                return flag
        return None


class FlagShipService:
    def __init__(self, repo: FlagShipRepo | None = None) -> None:
        self.repo = repo or FlagShipRepo()

    def create_flag(
        self,
        name: str,
        value: bool,
        desc: str | None = None,
        exp_unit: EXP_UNIT_T = "w",
        exp_value: int = 4,
    ) -> Flag:
        """
        Create a new `Flag` with the provided `name`, `value`, `desc`, `exp_unit` and `exp_value`.
        """
        expiration_date = new_expiration_date_from_now(unit=exp_unit, value=exp_value)
        new_flag = Flag(
            name=name, value=value, desc=desc, expiration_date=expiration_date
        )
        self.repo.save(flag=new_flag)
        return new_flag

    def get_flag(self, flag_id: str) -> Flag | None:
        return self.repo.store.get(flag_id)

    def is_enabled(self, name: str) -> bool:
        """
        Try to find the `Flag` by `name` and return its `value`.
        If the `Flag` is not found, raise a `ValueError`.
        """
        flag = self.repo.get_flag_by_name(name=name)
        if flag is None:
            raise FlagNotFoundException
        return False if flag.expired else flag.value

    def update_flag(self, flag_id: str, updated_fields: FlagAllowedUpdates) -> Flag:
        """
        Users can `update` existing `Flags` in their `store` by `id`.
        """
        if existing_flag := self.repo.store.get(flag_id):
            return self._update_flag(flag=existing_flag, updated_fields=updated_fields)
        raise FlagNotFoundException

    def delete_flag(self, flag_id: str) -> bool:
        """
        Users can `delete` existing `Flags` in their `store` by `id`.
        """
        if flag_id in self.repo.store:
            del self.repo.store[flag_id]
            return True
        return False

    def _update_flag(self, flag: Flag, updated_fields: FlagAllowedUpdates) -> Flag:
        """
        Internal method to update a flag with the provided fields.
        """
        for key, value in updated_fields.items():
            if value is not None:
                setattr(flag, key, value)

        self.repo.save(flag)
        return flag

    def get_all_flags(self, flag_name: str | None = None) -> list[Flag] | None:
        if flag_name:
            flag = self.repo.get_flag_by_name(name=flag_name)
            return [flag] if flag else []
        return [flag for flag in self.repo.store.values()]
