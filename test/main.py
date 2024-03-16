from httpx import AsyncClient

from app.main import app
from test.seeders.all_seeder import AllSeeder


class MainTest:

    def __init__(
            self,
            all_seeder: AllSeeder
    ):
        self.all_seeder = all_seeder
        self.client = AsyncClient(app=app, base_url="http://test")
