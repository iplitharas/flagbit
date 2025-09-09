from fastapi.testclient import TestClient
import pytest
from src.services.flagship import FlagShipService
from src.api.routers import app

from typing import Callable
from faker import Faker
from src.api.dependencies import get_flagship_service


@pytest.fixture(scope="module")
def fake_service() -> FlagShipService:
    flagship = FlagShipService()
    # update this with a fake dependency for testing
    app.dependency_overrides[get_flagship_service] = lambda : flagship
    return flagship

@pytest.fixture(scope="module")
def client(fake_service):
    with TestClient(app) as c:
        yield c


@pytest.fixture
def fake_flags_fixture(fake_service) -> Callable:
    """
    Fixture to create fake flags for testing.
    """
    def __fake_flag_fixture(num_flags: int = 3) -> None:
        fake = Faker()
        for _ in range(num_flags):
            fake_service.create_flag(
                name=fake.name(), value=fake.boolean(), desc=fake.sentence()
            )

    return __fake_flag_fixture
