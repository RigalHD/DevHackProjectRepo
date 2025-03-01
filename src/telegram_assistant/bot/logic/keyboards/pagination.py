from typing import Any

from aiogram.types import InlineKeyboardButton


def pagination(
    models: list[Any],
    switch_page_buttons: list[InlineKeyboardButton],
    page: int,
    models_per_page: int = 5,
) -> tuple[tuple[Any], tuple[InlineKeyboardButton]]:
    """
    Предназначается для удобной паггинации клавиатур aiogram
    :param models: список элементов для паггинации
    :switch_page_buttons: Кнопки для переключения страниц по шаблону [<Кнопка cлед. стр.>, <Кнопка пред. стр.>]
    :param page: Номер страницы
    :return: Возращает кортеж из элементов и кнопок для текущей страницы
    """
    switch_page_buttons = switch_page_buttons.copy()

    if models:
        result_models = models.copy()
        if len(models) > models_per_page:
            if page == 1:
                result_models = result_models[: page * models_per_page]
                switch_page_buttons.pop(1)
            elif 0 <= (page * models_per_page) - len(models) <= models_per_page:
                result_models = models[(page - 1) * models_per_page :]
                switch_page_buttons.pop(0)
            else:
                result_models = models[(page - 1) * models_per_page : page * models_per_page]
                switch_page_buttons = switch_page_buttons[::-1]
        else:
            result_models = result_models[:models_per_page]
            switch_page_buttons.clear()

        return (result_models, tuple(switch_page_buttons))
