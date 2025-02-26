from aiogram.filters.callback_data import CallbackData


class AdminPanelCBData(CallbackData, prefix="admin_panel"):
    action: str
