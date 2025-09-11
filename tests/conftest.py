from typing import Callable

import pytest
import pytest_asyncio
from faker import Faker
from fastapi.testclient import TestClient

from src.api.app import app
from src.api.dependencies import get_flagship_service
from src.repo.fake_repo import FakeInMemoryRepo
from src.services.flagship import FlagShipService


@pytest.fixture(scope="module")
def fake_service() -> FlagShipService:
    flagship = FlagShipService(repo=FakeInMemoryRepo())
    # update this with a fake dependency for testing
    app.dependency_overrides[get_flagship_service] = lambda: flagship
    return flagship


@pytest.fixture(scope="module")
def client(fake_service):
    with TestClient(app) as c:
        yield c


@pytest_asyncio.fixture
async def fake_flags_fixture(fake_service) -> Callable:
    """
    Fixture to create fake flags for testing.
    """

    async def __fake_flag_fixture(num_flags: int = 3) -> None:
        fake = Faker()
        for _ in range(num_flags):
            await fake_service.create_flag(
                name=fake.name(), value=fake.boolean(), desc=fake.sentence()
            )

    return __fake_flag_fixture
