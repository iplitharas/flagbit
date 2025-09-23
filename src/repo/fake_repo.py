from src.domain.flag import Flag
from src.exceptions import NotFoundError


class FakeInMemoryRepo:
    def __init__(self) -> None:
        self.mem_store: dict[str, Flag] = {}

    async def store(self, flag: Flag) -> None:
        """
        Store a new Flag in the repository.
        """
        self.mem_store[flag.id] = flag

    async def get_by_id(self, _id: str) -> Flag | None:
        """
        Retrieve a Flag by its ID from the repository.
        """
        flag = self.mem_store.get(_id)
        if flag:
            return flag
        error_msg = f"Flag with id: `{_id}` not found."
        raise NotFoundError(error_msg) from None

    async def get_by_name(self, name: str) -> Flag | None:
        """
        Retrieve a Flag by its name from the repository.
        """
        for flag in self.mem_store.values():
            if flag.name == name:
                return flag
        return None

    async def get_all(self, limit: int = 100) -> list[Flag]:
        """
        Retrieve all Flags from the repository, up to the specified limit.
        """
        return list(self.mem_store.values())[:limit]

    async def update(self, flag: Flag) -> Flag:
        """
        Update an existing Flag in the repository.
        """
        if flag.id in self.mem_store:
            self.mem_store[flag.id] = flag
            return flag
        error_msg = f"Flag with id: `{flag.id}` not found for update."
        raise NotFoundError(error_msg) from None

    async def delete(self, _id: str) -> None:
        """
        Delete a Flag by its ID from the repository.
        """
        if _id in self.mem_store:
            del self.mem_store[_id]
            return
        error_msg = f"Flag with id `{_id}` not found for deletion."
        raise NotFoundError(error_msg)
