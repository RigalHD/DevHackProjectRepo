from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine

from telegram_assistant.database.repositories import (
    BotAdministratorsRepository,
    TelegramUsersRepository,
)


def create_async_engine(url: URL | str) -> AsyncEngine:
    return _create_async_engine(url=url, echo=True, pool_pre_ping=True)


class Database:
    def __init__(
        self,
        session: AsyncSession,
        telegram_users: TelegramUsersRepository = None,
        bot_administrators: BotAdministratorsRepository = None,
        ) -> None:

        self.telegram_users: TelegramUsersRepository =\
            telegram_users or TelegramUsersRepository(session=session)
        self.bot_administrators: BotAdministratorsRepository =\
            bot_administrators or BotAdministratorsRepository(session=session)
        self.session: AsyncSession = session
