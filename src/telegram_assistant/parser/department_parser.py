import requests
from bs4 import BeautifulSoup

DEPARTMENT = "http://www.mmcs.sfedu.ru/faculty/departments"


class DepartmentParser:
    def parse_department(self) -> dict[str, str]:
        """
        Возвращает словарь c такой структурой:
        ключ - Название кафедры,
        значение - URL-адрес самой кафедры.
        """
        departments: dict[str, str] = {}

        response = requests.get(DEPARTMENT)

        bs = BeautifulSoup(response.text, "html.parser")

        list_div = bs.find("div", class_="newsitem_text")

        department_list = list_div.find_all("ul")

        for list in department_list:
            lis = list.find_all("li")

            for li in lis:
                a = li.find("a")
                departments[a.get_text()] = a.get("href")

            for link_key in departments:
                link = departments[link_key]
                if not link.startswith("http://sfedu.ru/") and not link.startswith("http://www.mmcs.sfedu.ru"):
                    new_link = "http://www.mmcs.sfedu.ru" + link
                    departments[link_key] = new_link

        return departments

    def parse_department_page(self, url: str) -> str:
        """
        :param url: Ссылка на URL страницы кафедры
        Парсит сайт кафедры (Возвращает строку)
        """
        department_links = self.parse_department()

        for link_key in department_links:
            link = department_links[link_key]

            if link == url:
                response = requests.get(link, timeout=10)

                bs = BeautifulSoup(response.text, "html.parser")

                if "://sfedu.ru" in link:
                    return link
                info_block = bs.find("div", class_="newsitem_text")
                imgs = info_block.find_all("img")
                for img in imgs:
                    img.decompose()
                text = info_block.get_text()

                return text
