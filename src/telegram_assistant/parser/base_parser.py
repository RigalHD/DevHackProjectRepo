from telegram_assistant.parser.parser import Parser


class BaseParser(Parser):
    def parse(self, *args, **kwargs) -> str: ...
