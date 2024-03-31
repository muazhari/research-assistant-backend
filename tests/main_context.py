from httpx import AsyncClient

from apps.main import app
from tests.seeders.all_seeder import AllSeeder


class MainContext:

    def __init__(
            self,
            all_seeder: AllSeeder
    ):
        self.all_seeder = all_seeder
        self.client = AsyncClient(app=app, base_url="http://test")
