from telegram_assistant.parser.parser import Parser
from bs4 import BeautifulSoup, Comment, Script
import requests

LINK_ADMISSION_RULES = "https://sfedu.ru/www/stat_pages22.show?p=ABT/N8202/P"
LINK_ADMISSION_VECTOR = "https://sfedu.ru/www/stat_pages22.show?p=ABT/N8206/P"
LINK_ADMISSION_INSTRUCTION = "https://sfedu.ru/00_main_2010/abitur/abit_2024/Instr_test_2024.pdf"
LINK_ADMISSION_SCHEDULE_BAKALAVR_AND_SPECIALIST = "https://sfedu.ru/00_main_2010/abitur/abit_2024/rasp_bak.pdf"
LINK_ADMISSION_SCHEDULE_MAGISTRATURA = "https://sfedu.ru/00_main_2010/abitur/abit_2024/rasp_mag.pdf"
LINK_ADMISSION_SCHEDULE_ASPIRANTURA = "https://sfedu.ru/00_main_2010/abitur/abit_2024/rasp_asp.pdf"
LINK_ADMISSION_FOREIGN = "https://sfedu.ru/www/stat_pages22.show?p=ABT/N8216/P"

class BaseParser(Parser):
    def get_rules(self, html: bool = False) -> str:
        all_text = []

        response = requests.get(LINK_ADMISSION_RULES)

        bs = BeautifulSoup(response.text, "html.parser")

        all_text = bs.find_all(class_ = 'content_wrapper')

        uls = all_text[0].find_all("ul")

        if uls[5]:
            extra = uls[6].find_all_next()
            for code in extra[15:]:
                code.decompose()
        
        h4 = all_text[0].find("h4", id = "tit2")

        if h4:
            extra_prev = h4.find_all_next()
            for code in extra_prev[0:5]:
                code.decompose()
        
        hrs = all_text[0].find_all("hr")

        for hr in hrs:
            hr.decompose()
        
        if not html:
            return all_text[0].get_text()
        else:
            return all_text[0].prettify()
    
    def get_type_employee(self, url: str) -> str:
        """
        Принимает url преподавателя и возвращает текст с его описанием
        """
        response = requests.get(url, timeout=10)
        
        bs = BeautifulSoup(response.text, "html.parser")

        content = bs.find(class_ = "about_employee")

        imgs = content.find_all("img")

        for img in imgs:
            img.decompose()

        return content.get_text()
