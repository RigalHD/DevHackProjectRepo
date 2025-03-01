from telegram_assistant.parser.repository.parser_repo import ParserRepo


class ContextManager:
    def __init__(self):
        self.parser_repo = ParserRepo()
        self.questions_ids: dict[int, str] = {
            "1": "Расскажи о ЮФУ",
            "2": "Расскажи о поступлении в ЮФУ",
            "3": "Расскажи о последних мероприятих ЮФУ",
            }
        self.context_dictionary = {
            "Расскажи о поступлении в ЮФУ": "context_admission.txt",
            "Расскажи о последних мероприятих ЮФУ": "context_events.txt",
            "Расскажи о ЮФУ": "context_SFU_description.txt",
        }
        
    def create_base_context(self) -> None:
        admission = self.parser_repo.base_parser.parse_admission_rules()
        self.save_context(
            "Расскажи о поступлении в ЮФУ",
            admission
        )
        vk_events = self.parser_repo.vk_parser.parse_vk_wall_posts()
        self.save_context(
            "Расскажи о последних мероприятих ЮФУ",
            vk_events
        )
        university_info = self.parser_repo.base_parser.parse_university_info()
        self.save_context(
            "Расскажи о ЮФУ",
            university_info
        )
    
    def save_context(self, question: str, context: str) -> None:
        path = f"src/telegram_assistant/llm/context/{self.context_dictionary[question]}"
        with open(path, "w", encoding="utf-8") as file:
            file.write(context)

    def get_context(self, question: str) -> str:
        if not (question in self.context_dictionary.keys()):
            raise Exception("Контекст вопроса не найден")
        
        path = f"src/telegram_assistant/llm/context/{self.context_dictionary[question]}"
        with open(path, "r", encoding="utf-8") as file:
            context = file.read()
        
        return context

    def get_dynamic_context(self) -> str:
        ...