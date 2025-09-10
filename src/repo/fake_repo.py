from src.domain.flag import Flag
from asyncio import Future


class FakeInMemoryRepo:
    def __init__(self):
        self.store = {}

    async def store(self, flag: Flag) -> None:
        """
        Store a new Flag in the repository.
        """
        self.store[flag.id] = flag

    async def get_by_id(self, _id: str) -> Flag | None:
        """
        Retrieve a Flag by its ID from the repository.
        """
        return self.store.get(_id)

    async def get_by_name(self, name: str) -> Flag | None:
        """
        Retrieve a Flag by its name from the repository.
        """
        for flag in self.store.values():
            if flag.name == name:
                return flag
        return None

    async def get_all(self, limit: int = 100) -> list[Flag]:
        """
        Retrieve all Flags from the repository, up to the specified limit.
        """
        return list(self.store.values())[:limit]

    async def update(self, flag: Flag) -> bool:
        """
        Update an existing Flag in the repository.
        """
        if flag.id in self.store:
            self.store[flag.id] = flag
            return True
        return False

    async def delete(self, _id: str) -> bool:
        """
        Delete a Flag by its ID from the repository.
        """
        if _id in self.store:
            del self.store[_id]
            return True
        return False
