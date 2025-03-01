import requests
from bs4 import BeautifulSoup

ADMISSION_RULES_URL = "https://sfedu.ru/www/stat_pages22.show?p=ABT/N8202/P"


class BaseParser:
    def parse_admission_rules(self, html: bool = False) -> str:
        """
        :param html: False - возвращает результат в формате текста;
                     True - возвращает результат в формате HTML.
        """
        all_text = []

        response = requests.get(ADMISSION_RULES_URL)

        bs = BeautifulSoup(response.text, "html.parser")

        all_text = bs.find_all(class_="content_wrapper")

        uls = all_text[0].find_all("ul")

        if uls[5]:
            extra = uls[6].find_all_next()
            for code in extra[15:]:
                code.decompose()

        h4 = all_text[0].find("h4", id="tit2")

        if h4:
            extra_prev = h4.find_all_next()
            for code in extra_prev[0:5]:
                code.decompose()

        hrs = all_text[0].find_all("hr")

        for hr in hrs:
            hr.decompose()

        if not html:
            return all_text[0].get_text()
        return str(all_text[0].prettify())

    def parse_teacher_info(self, url: str) -> str:
        """Принимает url преподавателя и возвращает текст с его описанием"""
        response = requests.get(url, timeout=10)

        bs = BeautifulSoup(response.text, "html.parser")

        content = bs.find(class_="about_employee")

        imgs = content.find_all("img")

        for img in imgs:
            img.decompose()

        return content.get_text()

    def parse_department_page(self, url: str) -> str:
        """
        :param url: Ссылка на URL страницы кафедры
        Парсит сайт кафедры (Возвращает строку)
        """
        response = requests.get(url, timeout=10)

        bs = BeautifulSoup(response.text, "html.parser")

        if "://sfedu.ru" in url:
            return url
        info_block = bs.find("div", class_="newsitem_text")
        imgs = info_block.find_all("img")
        for img in imgs:
            img.decompose()
        text = info_block.get_text()

        return text
