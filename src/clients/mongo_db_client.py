from typing import Any, AsyncGenerator

from pymongo import AsyncMongoClient
import asyncio
from pydantic_settings import BaseSettings
from loguru import logger
from contextlib import asynccontextmanager

from pymongo.asynchronous import AsyncCollection


class MongoDBConfig(BaseSettings):
    uri: str = "mongodb://root:example@localhost:27017/flagship_db?authSource=admin"
    db: str = "flagship_db"
    collection: str = "flags"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class MongoDBAsyncClient:
    def __init__(
        self,
        config: MongoDBConfig | None = None,
        client: AsyncMongoClient | None = None,
    ):
        self.config = config or MongoDBConfig()
        self._client = client or AsyncMongoClient

    @asynccontextmanager
    async def get_client(
        self,
    ) -> AsyncGenerator[AsyncMongoClient | None | type[AsyncMongoClient], Any]:
        try:
            await self.connect()
            yield self._client

        finally:
            await self.close()

    async def _ensure_collection_exists(self) -> None:
        if self._client:
            db = self._client[self.config.db]
            existing_collections = await db.list_collection_names()
            if self.config.collection not in existing_collections:
                await db.create_collection(self.config.collection)
                logger.info(f"Collection '{self.config.collection}' created.")
            else:
                logger.info(f"Collection '{self.config.collection}' already exists.")
        else:
            logger.error("MongoDB client is not connected.")

    async def connect(self) -> None:
        """
        PyMongoDB uses connection pooling by default. When you create a MongoClient instance,
        https://pymongo.readthedocs.io/en/stable/faq.html#how-does-connection-pooling-work-in-pymongo
        Spawning a subprocess:
        https://pymongo.readthedocs.io/en/stable/faq.html#using-pymongo-with-multiprocessing
        """

        self._client = self._client(self.config.uri)
        await self._client.admin.command("ping")
        logger.info(f"Connected successfully to MongoDB with uri: {self.config.uri}")
        await self._ensure_collection_exists()

    async def close(self) -> None:
        if self._client:
            await self._client.close()
            logger.info("MongoDB connection closed")

    def get_flags_collection(self) -> AsyncCollection:
        if self._client:
            db = self._client[self.config.db]
            return db[self.config.collection]
        else:
            logger.error("MongoDB client is not connected.")
            return None


async def main():
    mongo_db_client = MongoDBAsyncClient()
    async with mongo_db_client.get_client() as client:
        if client:
            db = client[mongo_db_client.config.db]
            collection = db[mongo_db_client.config.collection]
            docs = await collection.find().to_list(100)
            logger.info(f"documents in the database: {docs}")
        else:
            logger.error("Failed to get MongoDB client")


if __name__ == "__main__":
    asyncio.run(main())
