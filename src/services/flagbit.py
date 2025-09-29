from datetime import datetime
from typing import TypedDict

from pytz import utc

from src._types import EXP_UNIT_T
from src.domain.flag import Flag
from src.exceptions import (
    FlagNotFoundError,
    FlagPersistenceError,
    RepositoryConnectionError,
    RepositoryNotFoundError,
)
from src.helpers import new_expiration_date
from src.repo.base import FlagsShipRepo


class FlagAllowedUpdates(TypedDict, total=False):
    name: str | None
    value: bool | None
    desc: str | None


class FlagBitService:
    def __init__(self, repo: FlagsShipRepo) -> None:
        self.repo = repo

    async def create_flag(
        self,
        name: str,
        value: bool,  # noqa: FBT001 Boolean-typed positional argument in function definition
        desc: str | None = None,
        exp_unit: EXP_UNIT_T = "w",
        exp_value: int = 4,
    ) -> Flag:
        """
        Create a new `Flag` with the provided `name`, `value`, `desc`, `exp_unit` and `exp_value`.
        """
        try:
            expiration_date = new_expiration_date(
                current_datetime=datetime.now(tz=utc), unit=exp_unit, value=exp_value
            )
            new_flag = Flag(name=name, value=value, desc=desc, expiration_date=expiration_date)
            await self.repo.store(flag=new_flag)
            return new_flag
        except RepositoryConnectionError:
            raise FlagPersistenceError from None

    async def get_flag(self, flag_id: str) -> Flag:
        """
        Get `Flag` by it's id.
        """
        try:
            return await self.repo.get_by_id(_id=flag_id)
        except RepositoryNotFoundError:
            raise FlagNotFoundError from None
        except RepositoryConnectionError:
            raise FlagPersistenceError from None

    async def is_enabled(self, name: str) -> bool | None:
        """
        Try to find the `Flag` by `name` and return its `value`.
        raises: `RepositoryNotFoundError` and `RepositoryConnectionError`
        """
        try:
            if flag := await self.repo.get_by_name(name=name):
                return False if flag.expired else flag.value

            return None
        except RepositoryNotFoundError:
            raise FlagNotFoundError from None
        except RepositoryConnectionError:
            raise FlagPersistenceError from None

    async def update_flag(self, flag_id: str, updated_fields: FlagAllowedUpdates) -> Flag:  # type: ignore[return]
        """
        Users can `update` existing `Flags` in their `store` by `id`.
        """
        try:
            if existing_flag := await self.repo.get_by_id(_id=flag_id):
                for key, value in updated_fields.items():
                    if value is not None:
                        setattr(existing_flag, key, value)
                existing_flag.date_updated = datetime.now(tz=utc)
                return await self.repo.update(existing_flag)
        except RepositoryNotFoundError:
            raise FlagNotFoundError from None
        except RepositoryConnectionError:
            raise FlagPersistenceError from None

    async def get_all_flags(
        self,
        flag_name: str | None = None,
        flag_value: bool | None = None,  # noqa: FBT001
        expired: bool | None = None,  # noqa: FBT001
    ) -> list[Flag] | None:
        try:
            flags = await self.repo.get_all(
                flag_name=flag_name,
                flag_value=flag_value,
            )
            if expired is not None:
                flags = [flag for flag in flags if flag.expired == expired]
            return flags
        except RepositoryConnectionError:
            raise FlagPersistenceError from None

    async def delete_flag(self, flag_id: str) -> None:
        """
        Users can `delete` existing `Flags` in their `store` by `id`.
        """
        try:
            await self.repo.delete(_id=flag_id)
        except RepositoryNotFoundError:
            err_msg = f"Flag with id: `{flag_id}` not found for deletion."
            raise FlagNotFoundError(err_msg) from None
        except RepositoryConnectionError:
            raise FlagPersistenceError from None
