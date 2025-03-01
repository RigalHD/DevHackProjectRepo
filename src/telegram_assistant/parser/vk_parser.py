from typing import Any

import requests

from telegram_assistant.config import Configuration


class VKParser:
    def parse_vk_group_info(self) -> dict:
        """
        Возвращает словарь c информацией o группе Вконтакте
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

    def parse_vk_wall_posts(self, posts_count: int = 50, is_dict: bool = False) -> dict[int, str] | str:
        """
        :param number: Указывает сколько постов нужно получить (Значение по умолчанию: 50);
        :param is_dict: True - возвращает словарь (КЛЮЧ - номер поста ЗНАЧЕНИЕ - текст поста),
                        False - возвращает строку c текстом всех постов.
        """
        config_vk = Configuration().vk

        posts: list[dict[str, Any]] = []
        posts_dict: dict[int, str] = {}  # Ключ - номер поста, значение - текст поста
        all_posts_text: str  # Тескт всех постов

        result_post = requests.get(
            "https://api.vk.com/method/wall.get",
            params={
                "owner_id": config_vk.owner_id,
                "access_token": config_vk.token,
                "v": "5.199",
                "count": posts_count,
                "domain": config_vk.group_domain,
            },
        )

        if not result_post:
            print(result_post.status_code, result_post.text)

        post = result_post.json()["response"]["items"]
        posts.extend(post)

        for get_post in posts:
            posts_dict[posts.index(get_post)] = get_post["text"].replace(" \n", "").replace("\n", "")

        all_posts_text = "  |  ".join(list(posts_dict.values()))

        if is_dict:
            return posts_dict

        return all_posts_text
