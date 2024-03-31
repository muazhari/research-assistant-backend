import asyncio
from asyncio import AbstractEventLoop

import pytest
import pytest_asyncio

from tests.containers.test_container import TestContainer


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop: AbstractEventLoop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def main_context(request: pytest.FixtureRequest):
    test_container: TestContainer = TestContainer()
    main_context = test_container.main_context()
    await main_context.all_seeder.up()
    yield main_context
    await main_context.all_seeder.down()
