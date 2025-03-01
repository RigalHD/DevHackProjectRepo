from telegram_assistant.parser.repository.parser_repo import ParserRepository


class ContextManager:
    def __init__(self) -> None:
        self.parser_repo = ParserRepository()
        self.questions_ids: dict[int, str] = {
            "1": "Расскажи о ЮФУ",
            "2": "Расскажи о поступлении в ЮФУ",
            "3": "Расскажи о последних мероприятиях ЮФУ\
                (Основываясь на данных, которые тебе предоставлены)\
                (Расскажи о них, но без таких строк 'В сообщении содержится информация о след мероприятиях ЮФУ')",
        }
        self.context_dictionary = {
            "1": "context_SFU_description.txt",
            "2": "context_admission.txt",
            "3": "context_events.txt",
        }

    def create_base_context(self) -> None:
        university_info = self.parser_repo.base_parser.parse_university_info()
        self.save_context(
            "1",
            university_info,
        )
        admission = self.parser_repo.base_parser.parse_admission_rules()
        self.save_context(
            "2",
            admission,
        )
        vk_events = self.parser_repo.vk_parser.parse_vk_wall_posts()
        self.save_context(
            "3",
            vk_events,
        )

    def save_context(self, question_id: str, context: str) -> None:
        path = f"src/telegram_assistant/llm/context/{self.context_dictionary[question_id]}"
        with open(path, "w", encoding="utf-8") as file:
            file.write(context)

    def get_context(self, question_id: str) -> str:
        if question_id not in self.context_dictionary.keys():
            raise Exception("Контекст вопроса не найден")

        path = f"src/telegram_assistant/llm/context/{self.context_dictionary[question_id]}"
        with open(path, encoding="utf-8") as file:
            context = file.read()

        return context

    def get_dynamic_context(self) -> str: ...
