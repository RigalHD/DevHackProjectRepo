from telegram_assistant.llm.context_manager import ContextManager
from telegram_assistant.llm.yandex_gpt import YandexGPT


class LLMRepository:
    def __init__(self) -> None:
        self.context_manager = ContextManager()
        self.llm = YandexGPT()
        
        self.already_answered_questions: dict[str, str] = {}
        
    def get_question_info(self, question: str) -> str:
        context = self.context_manager.get_context(question)
        
        if question not in self.already_answered_questions.keys():
            llm_answer = self.llm.run(
                user_text=question,
                context=context,
            )
            self.already_answered_questions[question] = llm_answer
        else:
            llm_answer = self.already_answered_questions[question]

        return llm_answer
    
    def get_dynamic_question_info(self, question: str, context: str) -> str:
        editted_context = context +\
            "Основываясь только на этой информации дай ответ на следующий вопрос."
        
        if question not in self.already_answered_questions.keys():
            llm_answer = self.llm.run(
                user_text=question,
                context=context,
            )
            self.already_answered_questions[question] = llm_answer
        else:
            llm_answer = self.already_answered_questions[question]

        return llm_answer