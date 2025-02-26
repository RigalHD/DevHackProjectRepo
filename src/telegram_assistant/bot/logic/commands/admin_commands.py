from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from telegram_assistant.database import Database

router = Router()


@router.message(Command("add_admin"), flags={"needed_perms_level": 4})
async def add_admin(message: Message, command: CommandObject, db: Database) -> None:
    try:
        user = await db.telegram_users.get(message.from_user.id)

        telegram_id, permissions_level = [int(arg) for arg in command.args.split()]

        if user.admin_profile.permissions_level >= permissions_level:
            await message.answer("Недостаточно прав")
            return

        await db.bot_administrators.create(
            telegram_id=telegram_id,
            permissions_level=permissions_level,
        )
    except Exception:
        await message.answer("Не удалось добавить администратора")
    else:
        await message.answer("Администратор добавлен")
