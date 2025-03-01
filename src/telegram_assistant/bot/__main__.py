import asyncio

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from telegram_assistant.bot.discpatcher import dp
from telegram_assistant.config import cfg


def on_startup() -> None:
    print("Бот запущен")


async def main() -> None:
    load_dotenv()
    bot = Bot(
        cfg.bot.token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dp.startup.register(on_startup)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
