import requests
from bs4 import BeautifulSoup

TEACHER_URL = "http://www.mmcs.sfedu.ru/faculty/staff"
DEPARTMENTS_URL = "http://www.mmcs.sfedu.ru/faculty/departments"


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

    def parse_departments(self) -> dict[str, str]:
        """
        Возвращает словарь c такой структурой:
        ключ - Название кафедры,
        значение - URL-адрес самой кафедры.
        """
        departments: dict[str, str] = {}

        response = requests.get(DEPARTMENTS_URL)

        bs = BeautifulSoup(response.text, "html.parser")

        list_div = bs.find("div", class_="newsitem_text")

        department_list = list_div.find_all("ul")

        for lst in department_list:
            lis = lst.find_all("li")

            for li in lis:
                a = li.find("a")
                departments[a.get_text()] = a.get("href")

            for url_key in departments.keys():
                url = departments[url_key]
                if not url.startswith("http://sfedu.ru/") and not url.startswith("http://www.mmcs.sfedu.ru"):
                    new_link = "http://www.mmcs.sfedu.ru" + url
                    departments[url_key] = new_link

        return departments
