from aiogram import F, Router
from aiogram.types import CallbackQuery

from telegram_assistant.bot.logic.callbackdata import MainMenuCBData
from telegram_assistant.bot.logic.keyboards.inline import admin_panel_kb, main_menu_kb
from telegram_assistant.database import Database

router = Router()


@router.callback_query(MainMenuCBData.filter(F.action == "AdminPanelView"), flags={"needed_perms_level": 0})
async def admin_panel_handler(query: CallbackQuery) -> None:
    await query.message.edit_text(
        text="Админ-панель",
        reply_markup=admin_panel_kb(),
    )


@router.callback_query(MainMenuCBData.filter(F.action == "BackToMainMenu"))
async def back_to_main_menu_handler(query: CallbackQuery, db: Database) -> None:
    message_text = \
        f"<b>Приветствуем, {query.from_user.first_name}</b>\n\n"

    user = await db.telegram_users.get(query.from_user.id)

    await query.message.edit_text(
        text=message_text,
        reply_markup=main_menu_kb(user.admin_profile),
    )
