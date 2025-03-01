from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload

from telegram_assistant.bot.logic.keyboards.inline import main_menu_kb

from telegram_assistant.llm.llm_repo import LLMRepository
from telegram_assistant.parser.repository.parser_repo import ParserRepository

router = Router()

@router.message(CommandStart(deep_link=True))
async def start_with_deep_link(
    message: Message, 
    command: CommandObject,
    parse_repo: ParserRepository,
    llm_repo: LLMRepository,
    ):
    try:
        if args := decode_payload(command.args):
            if args.startswith("teacher_"):
                url_start = "https://sfedu.ru/s7/person/ru/"
                teacher_id = args.lstrip("teacher_")
                context = parse_repo.base_parser.parse_teacher_info(url_start + teacher_id)
                teacher_info = llm_repo.get_dynamic_question_info(
                    question=f"Расскажи об этом учителе вкратце, ID={teacher_id}",
                    context=context + "Максимальная длина твоего ответа - 3000 символов. На айди вопроса не обращай внимание!"
                    )
                
                await message.answer(
                    text=teacher_info
                )
                
                
            
    except:
        await message.answer("Возникла ошибка")


@router.message(CommandStart())
async def start(message: Message) -> None:
    message_text = f"<b>Приветствую, {message.from_user.first_name}</b>"

    await message.answer(
        text=message_text,
        reply_markup=main_menu_kb(),
    )
