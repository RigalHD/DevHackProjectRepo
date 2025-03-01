import requests

from telegram_assistant.config import Configuration


class VKParser:
    def parse_vk_group_info(self) -> dict:
        """
        Возвращает словарь с информацией о группе Вконтакте
        """
        config_vk = Configuration().vk

        group_info: dict = {}

        request_unsorted_info = requests.get(
            "https://api.vk.com/method/groups.getAddresses",
            params={
                "owner_id": config_vk.owner_id,
                "access_token": config_vk.token,
                "group_id": config_vk.group_id,
                "v": "5.199",
            },
        )

        unsorted_info = request_unsorted_info.json()["response"]["items"][0]

        group_info["phone"] = unsorted_info["phone"]
        group_info["address"] = unsorted_info["address"]
        group_info["city"] = unsorted_info["city"]["title"]
        group_info["title"] = unsorted_info["title"]

        return group_info

    def parse_vk_wall_posts(self, number: int = 50, is_dict: bool = True) -> dict[int, str] | str:
        """
        :param isdict: True - возвращает словарь (КЛЮЧ - номер поста ЗНАЧЕНИЕ - текст поста)
                        False - возвращает строку с текстом всех постов
        :param number: Указывает сколько постов нужно получить (Значение по умолчанию: 50)
        """
        config_vk = Configuration().vk

        count: int = number  # Количество постов
        posts: list = []  # Список всех запарсенных постов
        posts_text_and_number: dict = {}  # Словарь с №Списка и Текстом
        text_list: list = []  # Список всего текса всех постов
        text: str  # Тескт всех постов

        result_post = requests.get(
            "https://api.vk.com/method/wall.get",
            params={
                "owner_id": config_vk.owner_id,
                "access_token": config_vk.token,
                "v": "5.199",
                "count": count,
                "domain": config_vk.group_domain,
            },
        )

        if not result_post:
            print(result_post.status_code, result_post.text)

        post = result_post.json()["response"]["items"]
        posts.extend(post)

        for get_post in posts:
            posts_text_and_number[posts.index(get_post)] = get_post["text"]
            text_list.append(get_post["text"])

        text = " ".join(text_list)

        if is_dict:
            return posts_text_and_number
        return text
