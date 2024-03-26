import asyncio
from asyncio import AbstractEventLoop

import pytest
import pytest_asyncio
from httpx import AsyncClient

from apps.main import app
from tests.containers.test_container import TestContainer
from tests.seeders.all_seeder import AllSeeder


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop: AbstractEventLoop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def main_test(request: pytest.FixtureRequest):
    test_container: TestContainer = TestContainer()
    main_test = MainTest(
        all_seeder=test_container.seeders.all_seeder()
    )
    await main_test.all_seeder.up()
    yield main_test
    await main_test.all_seeder.down()


class MainTest:

    def __init__(
            self,
            all_seeder: AllSeeder
    ):
        self.all_seeder = all_seeder
        self.client = AsyncClient(app=app, base_url="http://test")
