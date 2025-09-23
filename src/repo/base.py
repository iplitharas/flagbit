from typing import Protocol, runtime_checkable

from src.domain.flag import Flag


@runtime_checkable
class FlagsShipRepo(Protocol):
    async def store(self, flag: Flag) -> None:
        """
        Store a new Flag in the repository.
        raises: `ServerSelectionTimeoutError` if the database server is unreachable.
        """
        raise NotImplementedError

    async def get_by_id(self, _id: str) -> Flag:
        """
        Retrieve a Flag by its ID from the repository.
        raises: `RepoNotFoundError` if the Flag with the given ID does not exist.
        raises: `ServerSelectionTimeoutError` if the database server is unreachable.
        """
        raise NotImplementedError

    async def get_by_name(self, name: str) -> Flag:
        """
        Retrieve a Flag by its name from the repository.
            raises: `RepoNotFoundError` if the Flag with the given name does not exist.
        raises: `ServerSelectionTimeoutError` if the database server is unreachable.
        """
        raise NotImplementedError

    async def get_all(self, limit: int = 100) -> list[Flag]:
        """
        Retrieve all Flags from the repository, up to the specified limit.
        raises: `ServerSelectionTimeoutError` if the database server is unreachable.
        """
        raise NotImplementedError

    async def update(self, flag: Flag) -> Flag:
        """
        Update an existing Flag in the repository.
        raises: `ServerSelectionTimeoutError` if the database server is unreachable.
        """
        raise NotImplementedError

    async def delete(self, _id: str) -> None:
        """
        Delete a Flag by its ID from the repository.
        raises: `RepoNotFoundError` if the Flag with the given ID does not exist.
        raises: `ServerSelectionTimeoutError` if the database server is unreachable.
        """
        raise NotImplementedError

    async def delete_all(self) -> None:
        """
        Delete all Flags from the repository.
        raises: `ServerSelectionTimeoutError` if the database server is unreachable.
        """
        raise NotImplementedError
