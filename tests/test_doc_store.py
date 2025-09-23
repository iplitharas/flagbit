"""
Test cases for `doc_store.py`.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.domain.flag import Flag
from src.exceptions import NotFoundError
from src.repo.doc_store import DocStoreRepo, MongoDBAsyncClient, flag_to_document


@pytest.mark.asyncio
async def test_doc_store_delete_all_method():
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
    assert result is None, "delete_all should not raise an exception in good path"


@pytest.mark.asyncio
async def test_doc_store_delete_method_with_valid_id():
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
    assert result is None, "delete should not raise an exception in good path"


@pytest.mark.asyncio
async def test_doc_store_delete_method_with_invalid_id():
    """
    Given a `DocumentStore` instance with it's `MongoDBAsyncClient` mocked
    When I call, the `delete` method with an invalid ID.
    Then I'm expecting the `delete_one` method of the collection to be called once with the correct filter
          and an `NotFoundError` to be raised.
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
    with pytest.raises(NotFoundError):
        result = await doc_store.delete(_id=invalid_id)

    # Then
    assert fake_collection.delete_one.call_count == 1, "delete_one was not called exactly once"
    assert fake_collection.delete_one.call_args[0][0] == {"_id": invalid_id}, (
        "delete_one was not called with the correct filter"
    )



@pytest.mark.asyncio
async def test_doc_store_update_method_with_existing_flag():
    """
    Given a `DocumentStore` instance with it's `MongoDBAsyncClient` mocked
    When I call the `update` method with an existing Flag.
    Then I'm expecting the `replace_one` method of the collection to be called
         once with the correct filter and document.
    """

    # Given
    mocked_client = MagicMock(spec=MongoDBAsyncClient)
    # Create a fake result for replace_one
    fake_result = MagicMock()
    fake_result.modified_count = 1
    # Create a fake collection with the ` replace_one ` method
    fake_collection = MagicMock()
    # Wire up the replace_one method to be an AsyncMock
    fake_collection.replace_one = AsyncMock(return_value=fake_result)
    mocked_client.get_flags_collection.return_value = fake_collection
    doc_store = DocStoreRepo(client=mocked_client)
    existing_flag = Flag(name="test_flag", value=True)

    # When
    result = await doc_store.update(flag=existing_flag)

    # Then
    assert fake_collection.replace_one.call_count == 1, "replace_one was not called exactly once"
    assert fake_collection.replace_one.call_args[0][0] == {"_id": str(existing_flag.id)}, (
        "replace_one was not called with the correct filter"
    )
    assert fake_collection.replace_one.call_args[0][1] == flag_to_document(existing_flag), (
        "replace_one was not called with the correct document"
    )
    assert result == existing_flag, "update did not return the expected Flag"


@pytest.mark.asyncio
async def test_doc_store_store_method():
    """
    Given a `DocStoreRepo` instance with its `MongoDBAsyncClient` mocked
    When I call the `store` method with a new Flag
    Then I'm expecting the `insert_one` method of the collection to be called once with the correct document
    """
    # Given
    mocked_client = MagicMock(spec=MongoDBAsyncClient)
    # Create a fake collection with the `insert_one` method
    fake_collection = MagicMock()
    # Wire up the insert_one method to be an AsyncMock
    fake_collection.insert_one = AsyncMock()
    mocked_client.get_flags_collection.return_value = fake_collection
    doc_store = DocStoreRepo(client=mocked_client)
    new_flag = Flag(name="new_flag", value=True)

    # When
    await doc_store.store(flag=new_flag)

    # Then
    assert fake_collection.insert_one.call_count == 1, "insert_one was not called exactly once"
    assert fake_collection.insert_one.call_args[0][0] == flag_to_document(new_flag), (
        "insert_one was not called with the correct document"
    )


@pytest.mark.asyncio
async def test_doc_store_get_by_id_method_with_valid_id():
    """
    Given a `DocStoreRepo` instance with its `MongoDBAsyncClient` mocked
    When I call the `get_by_id` method with an existing Flag ID
    Then I'm expecting the `find_one` method of the collection to be called once with the correct
         filter and the corresponding Flag to be returned
    """
    # Given
    mocked_client = MagicMock(spec=MongoDBAsyncClient)
    existing_flag = Flag(name="existing_flag", value=True)
    existing_flag_doc = flag_to_document(existing_flag)
    # Create a fake collection with the `find_one` method
    fake_collection = MagicMock()
    # Wire up the find_one method to be an AsyncMock returning the existing flag document
    fake_collection.find_one = AsyncMock(return_value=existing_flag_doc)
    mocked_client.get_flags_collection.return_value = fake_collection
    doc_store = DocStoreRepo(client=mocked_client)

    # When
    result = await doc_store.get_by_id(_id=str(existing_flag.id))

    # Then
    assert fake_collection.find_one.call_count == 1, "find_one was not called exactly once"
    assert fake_collection.find_one.call_args[0][0] == {"_id": str(existing_flag.id)}, (
        "find_one was not called with the correct filter"
    )
    assert result == existing_flag, "get_by_id did not return the expected Flag"


@pytest.mark.asyncio
async def test_doc_store_get_by_id_method_with_invalid_id():
    """
    Given a `DocStoreRepo` instance with its `MongoDBAsyncClient` mocked
    When I call the `get_by_id` method with a non-existing Flag ID
    Then I'm expecting the `find_one` method of the collection to be called once with the correct filter
         and None to be returned
    """
    # Given
    mocked_client = MagicMock(spec=MongoDBAsyncClient)
    # Create a fake collection with the `find_one` method
    fake_collection = MagicMock()
    # Wire up the find_one method to be an AsyncMock returning None
    fake_collection.find_one = AsyncMock(return_value=None)
    mocked_client.get_flags_collection.return_value = fake_collection
    doc_store = DocStoreRepo(client=mocked_client)
    non_existing_id = "non_existing_id"

    # When
    result = await doc_store.get_by_id(_id=non_existing_id)

    # Then
    assert fake_collection.find_one.call_count == 1, "find_one was not called exactly once"
    assert fake_collection.find_one.call_args[0][0] == {"_id": non_existing_id}, (
        "find_one was not called with the correct filter"
    )
    assert result is None, "get_by_id did not return None for non-existing ID"


@pytest.mark.asyncio
async def test_doc_store_get_by_name_method_with_valid_name():
    """
    Given a `DocStoreRepo` instance with its `MongoDBAsyncClient` mocked
    When I call the `get_by_name` method with an existing Flag name
    Then I'm expecting the `find_one` method of the collection to be called once with the correct
         filter and the corresponding Flag to be returned
    """
    # Given
    mocked_client = MagicMock(spec=MongoDBAsyncClient)
    existing_flag = Flag(name="existing_flag", value=True)
    existing_flag_doc = flag_to_document(existing_flag)
    # Create a fake collection with the `find_one` method
    fake_collection = MagicMock()
    # Wire up the find_one method to be an AsyncMock returning the existing flag document
    fake_collection.find_one = AsyncMock(return_value=existing_flag_doc)
    mocked_client.get_flags_collection.return_value = fake_collection
    doc_store = DocStoreRepo(client=mocked_client)

    # When
    result = await doc_store.get_by_name(name=existing_flag.name)

    # Then
    assert fake_collection.find_one.call_count == 1, "find_one was not called exactly once"
    assert fake_collection.find_one.call_args[0][0] == {"name": existing_flag.name}, (
        "find_one was not called with the correct filter"
    )
    assert result == existing_flag, "get_by_name did not return the expected Flag"


@pytest.mark.asyncio
async def test_doc_store_get_by_name_method_with_invalid_name():
    """
    Given a `DocStoreRepo` instance with its `MongoDBAsyncClient` mocked
    When I call the `get_by_name` method with a non-existing Flag name
    Then I'm expecting the `find_one` method of the collection to be called once with the correct filter
         and None to be returned
    """
    # Given
    mocked_client = MagicMock(spec=MongoDBAsyncClient)
    # Create a fake collection with the `find_one` method
    fake_collection = MagicMock()
    # Wire up the find_one method to be an AsyncMock returning None
    fake_collection.find_one = AsyncMock(return_value=None)
    mocked_client.get_flags_collection.return_value = fake_collection
    doc_store = DocStoreRepo(client=mocked_client)
    non_existing_name = "non_existing_name"

    # When
    result = await doc_store.get_by_name(name=non_existing_name)

    # Then
    assert fake_collection.find_one.call_count == 1, "find_one was not called exactly once"
    assert fake_collection.find_one.call_args[0][0] == {"name": non_existing_name}, (
        "find_one was not called with the correct filter"
    )
    assert result is None, "get_by_name did not return None for non-existing name"


@pytest.mark.asyncio
async def test_doc_store_get_all_method_returns_all_flags_if_limit_existing_flags_are_less_than_default_limit():
    """
    Given a `DocStoreRepo` instance with its `MongoDBAsyncClient` mocked
    When I call the `get_all` method
    Then I'm expecting the `find` method of the collection to be called once and a list of Flags to be returned
    """
    # Given
    mocked_client = MagicMock(spec=MongoDBAsyncClient)
    flag1 = Flag(name="flag1", value=True)
    flag2 = Flag(name="flag2", value=False)
    flag_docs = [flag_to_document(flag1), flag_to_document(flag2)]
    # Create a fake collection with the `find` method
    fake_collection = MagicMock()
    # Wire up the find method to be an AsyncMock returning a list of flag documents
    fake_collection.find = MagicMock()
    fake_collection.find.return_value.to_list = AsyncMock(return_value=flag_docs)
    mocked_client.get_flags_collection.return_value = fake_collection
    doc_store = DocStoreRepo(client=mocked_client)

    # When
    result = await doc_store.get_all()

    # Then
    assert fake_collection.find.call_count == 1, "find was not called exactly once"
    assert result == [flag1, flag2], "get_all did not return the expected list of Flags"


@pytest.mark.asyncio
async def test_doc_store_get_all_method_returns_empty_list_if_no_flags_exist():
    """
    Given a `DocStoreRepo` instance with its `MongoDBAsyncClient` mocked
    When I call the `get_all` method
    Then I'm expecting the `find` method of the collection to be called once and an empty list to be returned
    """
    # Given
    mocked_client = MagicMock(spec=MongoDBAsyncClient)
    # Create a fake collection with the `find` method
    fake_collection = MagicMock()
    # Wire up the find method to be an AsyncMock returning an empty list
    fake_collection.find = MagicMock()
    fake_collection.find.return_value.to_list = AsyncMock(return_value=[])
    mocked_client.get_flags_collection.return_value = fake_collection
    doc_store = DocStoreRepo(client=mocked_client)

    # When
    result = await doc_store.get_all()

    # Then
    assert fake_collection.find.call_count == 1, "find was not called exactly once"
    assert result == [], "get_all did not return an empty list when no Flags exist"
