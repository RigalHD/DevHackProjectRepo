from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage

from telegram_assistant.bot.logic import logic_routers
from telegram_assistant.bot.middlewares import routers as middlewares_routers
from telegram_assistant.bot.middlewares.db_middleware import DatabaseMiddleware
from telegram_assistant.bot.middlewares.perms_check_middleware import PermissionsCheckMiddleware
from telegram_assistant.bot.middlewares.register_check_middleware import RegistrationCheckMiddleware

storage: BaseStorage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_routers(
    *logic_routers,
    *middlewares_routers,
)

dp.message.middleware(DatabaseMiddleware())
dp.callback_query.middleware(DatabaseMiddleware())
dp.message.middleware(RegistrationCheckMiddleware())
dp.callback_query.middleware(RegistrationCheckMiddleware())
dp.message.middleware(PermissionsCheckMiddleware())
dp.callback_query.middleware(PermissionsCheckMiddleware())
