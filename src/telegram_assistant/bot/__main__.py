import asyncio

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from telegram_assistant.bot.discpatcher import dp
from telegram_assistant.config import cfg
from telegram_assistant.llm.context_manager import ContextManager
from telegram_assistant.llm.llm_repo import LLMRepository


def on_startup() -> None:
    print("Бот запущен")


async def main() -> None:
    llm_repo = LLMRepository()
    llm_repo.context_manager.create_base_context()
    bot = Bot(
        cfg.bot.token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dp.startup.register(on_startup)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, llm_repo=llm_repo)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
