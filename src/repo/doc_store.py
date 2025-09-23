"""
Implements a document storage repo for MongoDB.
"""

from dataclasses import asdict
from typing import TYPE_CHECKING, Any

from loguru import logger
from pymongo.errors import ServerSelectionTimeoutError

from src.exceptions import RepoNotFoundError, RepositoryConnError

if TYPE_CHECKING:
    from pymongo.results import DeleteResult

from src.clients.mongo_db_client import MongoDBAsyncClient
from src.domain.flag import Flag

type MongoDBDocument = dict[str, Any]


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


class DocStoreRepo:
    def __init__(self, client: MongoDBAsyncClient | None = None) -> None:
        self._client = client or MongoDBAsyncClient()

    async def store(self, flag: Flag) -> None:
        """
        Store a new Flag document in the MongoDB collection.
        """
        coll = self._client.get_flags_collection()
        try:
            await coll.insert_one(flag_to_document(flag=flag))
        except ServerSelectionTimeoutError as error:
            logger.error(f"Failed to connect to MongoDB server: `{error}`")
            err_msg = "Cannot connect to the MongoDB server, during store operation."
            raise RepositoryConnError(err_msg) from None

    async def get_by_id(self, _id: str) -> Flag:
        """
        Retrieve a Flag document by its ID from the MongoDB collection.
        """
        coll = self._client.get_flags_collection()
        try:
            if document := await coll.find_one({"_id": _id}):
                return document_to_flag(doc=document)
            msg = f"Flag with id: `{_id}` not found."
            raise RepoNotFoundError(msg)
        except ServerSelectionTimeoutError as error:
            logger.error(f"Failed to connect to MongoDB server: `{error}`")
            err_msg = "Cannot connect to the MongoDB server, during get_by_id operation."
            raise RepositoryConnError(err_msg) from None

    async def get_by_name(self, name: str) -> Flag:
        """
        Retrieve a Flag document by its name from the MongoDB collection.
        """
        coll = self._client.get_flags_collection()
        try:
            if document := await coll.find_one({"name": name}):
                return document_to_flag(doc=document)
            msg = f"Flag with name: `{name}` not found."
            raise RepoNotFoundError(msg)
        except ServerSelectionTimeoutError as error:
            logger.error(f"Failed to connect to MongoDB server: `{error}`")
            err_msg = "Cannot connect to the MongoDB server, during get_by_name operation."
            raise RepositoryConnError(err_msg) from None

    async def get_all(self, limit: int = 100) -> list[Flag]:
        """
        Retrieve all Flag documents from the MongoDB collection, up to the specified limit.
        """
        coll = self._client.get_flags_collection()
        try:
            documents = await coll.find().to_list(limit)
            return [document_to_flag(doc=document) for document in documents]
        except ServerSelectionTimeoutError as error:
            logger.error(f"Failed to connect to MongoDB server: `{error}`")
            err_msg = "Cannot connect to the MongoDB server, during get_all operation."
            raise RepositoryConnError(err_msg) from None

    async def update(self, flag: Flag) -> Flag:
        """
        Update an existing Flag document in the MongoDB collection.
        """
        collection = self._client.get_flags_collection()
        try:
            result = await collection.replace_one({"_id": str(flag.id)}, flag_to_document(flag))
            if result.matched_count == 0:
                err_msg = f"Flag with id: `{flag.id}` not found for update."
                raise RepoNotFoundError(err_msg)

            return flag  # noqa: TRY300
        except ServerSelectionTimeoutError as error:
            logger.error(f"Failed to connect to MongoDB server: `{error}`")
            err_msg = "Cannot connect to the MongoDB server, during update operation."
            raise RepositoryConnError(err_msg) from None

    async def delete(self, _id: str) -> None:
        """
        Delete a Flag document by its ID from the MongoDB collection.
        """
        collection = self._client.get_flags_collection()
        try:
            result: DeleteResult = await collection.delete_one({"_id": _id})
            if result.deleted_count == 0:
                err_msg = f"Flag with id `{_id}` not found for deletion."
                raise RepoNotFoundError(err_msg)
        except ServerSelectionTimeoutError as error:
            logger.error(f"Failed to connect to MongoDB server: `{error}`")
            err_msg = "Cannot connect to the MongoDB server, during delete operation."
            raise RepositoryConnError(err_msg) from None

    async def delete_all(self) -> None:
        """
        Delete all Flag documents from the MongoDB collection.
        """
        collection = self._client.get_flags_collection()
        try:
            result: DeleteResult = await collection.delete_many({})
            if result.deleted_count == 0:
                logger.warning("No documents found to delete.")
        except ServerSelectionTimeoutError as error:
            logger.error(f"Failed to connect to MongoDB server: `{error}`")
            err_msg = "Cannot connect to the MongoDB server, during delete_all operation."
            raise RepositoryConnError(err_msg) from None
