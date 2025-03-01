import requests

from telegram_assistant.config import Configuration


class YandexGPT:
    def __init__(self) -> None:
        self.llm_cfg = Configuration().llm
        self.api_key = self.llm_cfg.token
        self.folder_id = self.llm_cfg.folder_id

    def run(
        self,
        user_text: str,
        context: str,
        url: str = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
    ) -> str:
        data = {}
        data["modelUri"] = f"gpt://{self.folder_id}/yandexgpt"
        data["completionOptions"] = {"temperature": 0.1, "maxTokens": 1000}
        data["messages"] = [
            {"role": "system", "text": context},
            {"role": "user", "text": f"{user_text}"},
        ]

        response = requests.post(
            url,
            headers={"Accept": "application/json", "Authorization": f"Api-Key {self.api_key}"},
            json=data,
        ).json()
        
        return response["result"]["alternatives"][0]["message"]["text"]
