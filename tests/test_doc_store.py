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
    # Create a fake result for delete_many
    fake_result = MagicMock()
    fake_result.deleted_count = 1
    # Create a fake collection with `delete_many` method
    fake_collection = MagicMock()
    # Wire up the delete_many method to be an AsyncMock
    fake_collection.delete_many = AsyncMock(return_value=fake_result)
    mocked_client.get_flags_collection.return_value = fake_collection
    doc_store = DocStoreRepo(client=mocked_client)

    # When
    result = await doc_store.delete_all()

    # Then
    assert fake_collection.delete_many.call_count == 1, "delete_many was not called exactly once"
    assert fake_collection.delete_many.call_args[0][0] == {}, (
        "delete_many was not called with an empty filter"
    )
    assert result is True, "delete_all did not return True"


@pytest.mark.asyncio
async def test_document_store_delete_with_valid_id():
    """
    Given a `DocumentStore` instance with it's `MongoDBAsyncClient` mocked
    When I call, the `delete` method with a valid ID.
    Then I'm expecting the `delete_one` method of the collection to be called once with the correct filter.
    """
    # Given
    mocked_client = MagicMock(spec=MongoDBAsyncClient)
    # Create a fake result for delete_one
    fake_result = MagicMock()
    fake_result.deleted_count = 1
    # Create a fake collection with the ` delete_one ` method
    fake_collection = MagicMock()
    # Wire up the delete_one method to be an AsyncMock
    fake_collection.delete_one = AsyncMock(return_value=fake_result)
    mocked_client.get_flags_collection.return_value = fake_collection
    doc_store = DocStoreRepo(client=mocked_client)
    valid_id = "valid_id"

    # When
    result = await doc_store.delete(_id=valid_id)

    # Then
    assert fake_collection.delete_one.call_count == 1, "delete_one was not called exactly once"
    assert fake_collection.delete_one.call_args[0][0] == {"_id": valid_id}, (
        "delete_one was not called with the correct filter"
    )
    assert result is True, "delete did not return True"

    async def document_sore_delete_with_invalid_id():
        """
        Given a `DocumentStore` instance with it's `MongoDBAsyncClient` mocked
        When I call, the `delete` method with an invalid ID.
        Then I'm expecting the `delete_one` method of the collection to be called once with the correct filter.
        """
        # Given
        mocked_client = MagicMock(spec=MongoDBAsyncClient)
        # Create a fake result for delete_one
        fake_result = MagicMock()
        fake_result.deleted_count = 0
        # Create a fake collection with the ` delete_one ` method
        fake_collection = MagicMock()
        # Wire up the delete_one method to be an AsyncMock
        fake_collection.delete_one = AsyncMock(return_value=fake_result)
        mocked_client.get_flags_collection.return_value = fake_collection
        doc_store = DocStoreRepo(client=mocked_client)
        invalid_id = "invalid_id"

        # When
        result = await doc_store.delete(_id=invalid_id)

        # Then
        assert fake_collection.delete_one.call_count == 1, "delete_one was not called exactly once"
        assert fake_collection.delete_one.call_args[0][0] == {"_id": invalid_id}, (
            "delete_one was not called with the correct filter"
        )
        assert result is False, "delete did not return False"
