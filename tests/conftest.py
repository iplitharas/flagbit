from collections.abc import Callable

import pytest
import pytest_asyncio
from faker import Faker
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.dependencies import get_flagship_service
from src.api.flags_router import flags_router
from src.domain.flag import Flag
from src.repo.fake_repo import FakeInMemoryRepo
from src.services.flagship import FlagShipService


@pytest.fixture(scope="module")
def test_app() -> FastAPI:
    """
    Create a test FastAPI app with routers but no lifespan.
    """
    app = FastAPI(title="Test Feature Flag API")
    app.include_router(flags_router, tags=["Flags"])
    return app


@pytest.fixture(scope="module")
def client(test_app):
    with TestClient(test_app) as c:
        yield c


@pytest.fixture(scope="function")
def flagship_with_in_memory_repo():
    flagship_srv = FlagShipService(repo=FakeInMemoryRepo())
    return flagship_srv


@pytest.fixture(scope="function", autouse=True)
def override_get_flagship_service(test_app, flagship_with_in_memory_repo):
    test_app.dependency_overrides[get_flagship_service] = lambda: flagship_with_in_memory_repo
    yield
    test_app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def fake_flags_fixture(flagship_with_in_memory_repo) -> Callable:
    async def __fake_flag_fixture(num_flags: int = 3) -> list[Flag]:
        fake = Faker()
        flags = []
        for _ in range(num_flags):
            flags.append(
                await flagship_with_in_memory_repo.create_flag(
                    name=fake.name(), value=fake.boolean(), desc=fake.sentence()
                )
            )
        return flags

    return __fake_flag_fixture
