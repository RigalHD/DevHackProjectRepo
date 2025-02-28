from telegram_assistant.parser.parser import Parser
from bs4 import BeautifulSoup, Comment, Script
import requests

link_admission_rules = "https://sfedu.ru/www/stat_pages22.show?p=ABT/N8202/P"
link_admission_vector = "https://sfedu.ru/www/stat_pages22.show?p=ABT/N8206/P"
link_admission_instruction = "https://sfedu.ru/00_main_2010/abitur/abit_2024/Instr_test_2024.pdf"
link_admission_schedule_bakalavr_and_specialist = "https://sfedu.ru/00_main_2010/abitur/abit_2024/rasp_bak.pdf"
link_admission_schedule_magistratura = "https://sfedu.ru/00_main_2010/abitur/abit_2024/rasp_mag.pdf"
link_admission_schedule_aspirantura = "https://sfedu.ru/00_main_2010/abitur/abit_2024/rasp_asp.pdf"
link_admission_foreign = "https://sfedu.ru/www/stat_pages22.show?p=ABT/N8216/P"

class BaseParser(Parser):
    #(str - возвращает текст без тэгов, html - html код)
    def get_rules(self, return_what: str = "str") -> str:
        all_text = []

        response = requests.get(link_admission_rules)

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
        
        if return_what == "str":
            return all_text[0].get_text()
        elif return_what == "html":
            return all_text[0].prettify()
    
    #Принимает url преподавателя и возвращает текст с его описанием
    def get_type_employee(self, url: str) -> str:
        response = requests.get(url, timeout=10)
        
        bs = BeautifulSoup(response.text, "html.parser")

        content = bs.find(class_ = "about_employee")

        imgs = content.find_all("img")

        for img in imgs:
            img.decompose()

        return content.get_text()
