from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage

from telegram_assistant.bot.logic import logic_routers

storage: BaseStorage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_routers(
    *logic_routers,
)
