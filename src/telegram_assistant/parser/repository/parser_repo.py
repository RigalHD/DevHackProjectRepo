from telegram_assistant.parser.table_parser import TableParser
from typing import Any

class ParserRepo:
    def __init__(self) -> None:
        self.table_parser = TableParser()
        self.lite_table_parse_settings: dict[str, str | int] = {
            "url": "https://sfedu.ru/www/stat_pages22.show?p=ABT/N8206",
            "table_class": "sheet0 gridlines cke_show_border",
            "row_class_name": "row",
            "data_row_offset": 2,
        }
        self.parse_specific_row_settings: dict[str, str] = {
            "url": "https://sfedu.ru/www/stat_pages22.show?p=ABT/N8206",
            "table_class": "sheet0 gridlines cke_show_border",
            "row_class_name": "row",
        }
    
    def parse_table(
        self,
        reversed_result: bool = True,
        table_number: int | None = None,
        changed_settings: dict[str, Any] | None = None
    ) -> dict[str, str]:
        settings = self.lite_table_parse_settings
        
        if changed_settings:
            settings = changed_settings
            
        result = self.table_parser.lite_parse_table(
            **settings,
            reversed_result=reversed_result,
            table_number=table_number
        )
        
        return result
    
    def parse_specific_row(
        self,
        row_number: int,
        table_number: int | None = None,
        changed_settings: dict[str, Any] | None = None
    ) -> dict[str, str | dict[str, str]]:
        settings = self.parse_specific_row_settings
        
        if changed_settings:
            settings = changed_settings
        
        result = self.table_parser.parse_specific_row(
            row_number=row_number,
            table_number=table_number,
            **settings,
        )
        
        return result
