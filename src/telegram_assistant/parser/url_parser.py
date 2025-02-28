import requests
from bs4 import BeautifulSoup

TEACHER_URL = "http://www.mmcs.sfedu.ru/faculty/staff"


class URLParser:
    def parse_teachers(self) -> dict[str, str]:
        """
        Возвращает словарь c такой структурой:
        ключ - ФИО учителя,
        значение - URL-адрес его профиля.
        """
        teachers: dict[str, str] = {}

        response = requests.get(TEACHER_URL)

        bs = BeautifulSoup(response.text, "html.parser")

        all_text = bs.find_all("ul", class_="staff_list")

        for data in all_text:
            for li in data.find_all("li"):
                teacher_name = li.get_text().strip()
                url = li.find("a").get("href")
                teachers[teacher_name] = url

        return teachers
