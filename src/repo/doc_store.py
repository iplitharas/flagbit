"""
Implements a document storage repo for MongoDB.
"""

from collections.abc import Awaitable, Callable
from dataclasses import asdict
from functools import wraps
from typing import TYPE_CHECKING, Any, TypeVar

from loguru import logger
from pymongo.errors import ServerSelectionTimeoutError

from src.exceptions import RepositoryConnectionError, RepositoryNotFoundError

if TYPE_CHECKING:
    from pymongo.results import DeleteResult

from src.clients.mongo_db_client import MongoDBAsyncClient
from src.domain.flag import Flag

type MongoDBDocument = dict[str, Any]

F = TypeVar("F", bound=Callable[..., Awaitable[Any]])


def flag_to_document(flag: Flag) -> MongoDBDocument:
    """
    Convert a Flag instance to a dictionary suitable for MongoDB storage.
    """
    doc = asdict(flag)
    doc["_id"] = doc.pop("id")
    return doc


def document_to_flag(doc: MongoDBDocument) -> Flag:
    """
    Convert a MongoDB document to a Flag instance.
    """
    return Flag(id=str(doc["_id"]), **{k: v for k, v in doc.items() if k != "_id"})


def handle_conn_error(fn: Callable[..., Awaitable[Any]]) -> Callable:  # type: ignore
    """
    Async decorator to handle MongoDB connection errors.
    """

    @wraps(fn)
    async def inner(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        try:
            return await fn(*args, **kwargs)
        except ServerSelectionTimeoutError as error:
            logger.error(f"Failed to connect to MongoDB server: `{error}`")
            err_msg = f"Cannot connect to MongoDB server during `{fn.__name__}`."
            raise RepositoryConnectionError(err_msg) from None

    return inner  # type ignore


class DocStoreRepo:
    def __init__(self, client: MongoDBAsyncClient | None = None) -> None:
        self._client = client or MongoDBAsyncClient()

    @handle_conn_error
    async def store(self, flag: Flag) -> None:
        """
        Store a new Flag document in the MongoDB collection.
        """
        coll = self._client.get_flags_collection()
        await coll.insert_one(flag_to_document(flag=flag))

    @handle_conn_error
    async def get_by_id(self, _id: str) -> Flag:
        """
        Retrieve a Flag document by its ID from the MongoDB collection.
        """
        coll = self._client.get_flags_collection()
        if document := await coll.find_one({"_id": _id}):
            return document_to_flag(doc=document)
        msg = f"Flag with id: `{_id}` not found."
        raise RepositoryNotFoundError(msg)

    @handle_conn_error
    async def get_by_name(self, name: str) -> Flag:
        """
        Retrieve a Flag document by its name from the MongoDB collection.
        """
        coll = self._client.get_flags_collection()
        if document := await coll.find_one({"name": name}):
            return document_to_flag(doc=document)
        msg = f"Flag with name: `{name}` not found."
        raise RepositoryNotFoundError(msg)

    @handle_conn_error
    async def get_all(
        self,
        flag_name: str | None = None,
        flag_value: bool | None = None,  # noqa: FBT001
        limit: int = 100,
    ) -> list[Flag]:
        """
        Retrieve all Flag documents from the MongoDB collection, up to the specified limit.
        """
        coll = self._client.get_flags_collection()
        filters: dict[str, str | bool] = {}
        if flag_name is not None:
            filters["name"] = flag_name
        if flag_value is not None:
            filters["value"] = flag_value

        logger.debug(f"Filtering flags with: {filters}")
        documents = await coll.find(filters).to_list(limit)

        return [document_to_flag(doc=document) for document in documents]

    @handle_conn_error
    async def update(self, flag: Flag) -> Flag:
        """
        Update an existing Flag document in the MongoDB collection.
        """
        collection = self._client.get_flags_collection()
        result = await collection.replace_one({"_id": str(flag.id)}, flag_to_document(flag))
        if result.matched_count == 0:
            err_msg = f"Flag with id: `{flag.id}` not found for update."
            raise RepositoryNotFoundError(err_msg)

        return flag

    @handle_conn_error
    async def delete(self, _id: str) -> None:
        """
        Delete a Flag document by its ID from the MongoDB collection.
        """
        collection = self._client.get_flags_collection()
        result: DeleteResult = await collection.delete_one({"_id": _id})
        if result.deleted_count == 0:
            err_msg = f"Flag with id `{_id}` not found for deletion."
            raise RepositoryNotFoundError(err_msg)

    @handle_conn_error
    async def delete_all(self) -> None:
        """
        Delete all Flag documents from the MongoDB collection.
        """
        collection = self._client.get_flags_collection()
        result: DeleteResult = await collection.delete_many({})
        if result.deleted_count == 0:
            logger.warning("No documents found to delete.")
