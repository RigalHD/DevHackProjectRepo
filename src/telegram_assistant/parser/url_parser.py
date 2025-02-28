from telegram_assistant.parser.parser import Parser
from bs4 import BeautifulSoup, Comment, Script
import requests

LINK_STAFF = "http://www.mmcs.sfedu.ru/faculty/staff"

class URLParser(Parser):
    def parse_staff_profile_link(self) -> dict:
        """
        Возвращает словарь с именем учителя как ключ и ссылки на его профиль как значение
        """
        staff = {}

        response = requests.get(LINK_STAFF)

        bs = BeautifulSoup(response.text, "html.parser")

        all_text = bs.find_all("ul", class_ = 'staff_list')

        for data in all_text:
            for li in data.find_all("li"):
                staff_name = li.get_text().strip()
                link = li.find("a").get("href")
                staff[staff_name] = link

        return staff