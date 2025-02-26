from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()


@dataclass
class DatabaseConfig:
    name: str | None = getenv("DATABASE_NAME")
    user: str | None = getenv("DATABASE_USER")
    passwd: str | None = getenv("DATABASE_PASSWORD", None)
    port: int = int(getenv("DATABASE_PORT", "5432"))
    host: str = getenv("DATABASE_HOST", "db")

    driver: str = "asyncpg"
    database_system: str = "postgresql"

    media_path: str = "database/media/"

    def build_connection_str(self) -> str:
        return URL.create(
            drivername=f"{self.database_system}+{self.driver}",
            username=self.user,
            database=self.name,
            password=self.passwd,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)


@dataclass
class BotConfig:
    token: str = getenv("BOT_TOKEN")


@dataclass
class Configuration:
    db = DatabaseConfig()
    bot = BotConfig()


cfg = Configuration()
