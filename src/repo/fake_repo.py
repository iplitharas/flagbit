from src.domain.flag import Flag
from src.exceptions import RepositoryNotFoundError


class FakeInMemoryRepo:
    def __init__(self) -> None:
        self.mem_store: dict[str, Flag] = {}

    async def store(self, flag: Flag) -> None:
        """
        Store a new Flag in the repository.
        """
        self.mem_store[flag.id] = flag

    async def get_by_id(self, _id: str) -> Flag:
        """
        Retrieve a Flag by its ID from the repository.
        """
        flag = self.mem_store.get(_id)
        if flag:
            return flag
        error_msg = f"Flag with id: `{_id}` not found."
        raise RepositoryNotFoundError(error_msg) from None

    async def get_by_name(self, name: str) -> Flag:
        """
        Retrieve a Flag by its name from the repository.
        """
        for flag in self.mem_store.values():
            if flag.name == name:
                return flag
        error_msg = f"Flag with name: `{name}` not found."
        raise RepositoryNotFoundError(error_msg)

    async def get_all(
        self,
        flag_name: str | None = None,
        flag_value: bool | None = None,  # noqa: FBT001
        limit: int = 100,
    ) -> list[Flag]:
        """
        Retrieve all Flags from the repository, up to the specified limit.
        """
        existing_flags = list(self.mem_store.values())
        if flag_name is not None:
            existing_flags = [flag for flag in existing_flags if flag.name == flag_name]
        if flag_value is not None:
            existing_flags = [flag for flag in existing_flags if flag.value == flag_value]
        if existing_flags:
            return existing_flags[:limit]
        return []

    async def update(self, flag: Flag) -> Flag:
        """
        Update an existing Flag in the repository.
        """
        if flag.id in self.mem_store:
            self.mem_store[flag.id] = flag
            return flag
        error_msg = f"Flag with id: `{flag.id}` not found for update."
        raise RepositoryNotFoundError(error_msg) from None

    async def delete(self, _id: str) -> None:
        """
        Delete a Flag by its ID from the repository.
        """
        if _id in self.mem_store:
            del self.mem_store[_id]
            return
        error_msg = f"Flag with id `{_id}` not found for deletion."
        raise RepositoryNotFoundError(error_msg)

    async def delete_all(self) -> None:
        """
        Delete all Flags from the repository.
        """
        self.mem_store = {}
