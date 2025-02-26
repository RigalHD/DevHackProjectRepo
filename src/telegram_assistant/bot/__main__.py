import asyncio

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from telegram_assistant.bot.discpatcher import dp
from telegram_assistant.config import cfg
from telegram_assistant.database.db import create_async_engine
from telegram_assistant.database.models import BaseModel


def on_startup() -> None:
    print("Бот запущен")


async def main() -> None:
    load_dotenv()
    bot = Bot(
        cfg.bot.token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    sqlalchemy_url = cfg.db.build_connection_str()
    async_engine = create_async_engine(sqlalchemy_url)
    dp.startup.register(on_startup)
    async with async_engine.begin() as conn:
        # await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, engine=async_engine)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
