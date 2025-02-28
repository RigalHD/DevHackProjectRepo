from telegram_assistant.parser.parser import Parser


class URLParser(Parser):
    def parse(self, *args, **kwargs) -> dict[str, str]: ...
