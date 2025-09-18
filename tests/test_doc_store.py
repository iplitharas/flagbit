"""
Test cases for `doc_store.py`.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.repo.doc_store import DocStoreRepo, MongoDBAsyncClient


@pytest.mark.asyncio
async def test_document_store_delete_all():
    """
    Given a `DocumentStore` instance with it's `MongoDBAsyncClient` mocked
    When I call, the `delete_all` method.
    Then I'm expecting the `delete_many` method of the collection to be called once with an empty filter.
    """
    # Given
    mocked_client = MagicMock(spec=MongoDBAsyncClient)

    fake_collection = MagicMock()

    fake_collection.delete_many = AsyncMock(return_value=1)
    mocked_client.get_flags_collection.return_value = fake_collection
    doc_store = DocStoreRepo(client=mocked_client)

    # When
    result = await doc_store.delete_all()

    # Then
    assert fake_collection.delete_many.call_count == 1, "delete_many was not called exactly once"
    assert fake_collection.delete_many.call_args[0][0] == {}, (
        "delete_many was not called with an empty filter"
    )
    assert result == 1, "delete_all should return 1"
