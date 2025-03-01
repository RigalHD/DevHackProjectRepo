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


# Это тест
# context_test = """Сроки проведения процедур приема и зачисления на обучение по программам магистратуры в 2025 году:
# На места в рамках контрольных цифр приема по всем формам обучения: Срок начала приема заявлений о приеме на обучение и документов, прилагаемых к заявлению - 20 июня;
# срок завершения приема документов от поступающих на обучение - 5 августа;
# сроки проведения вступительных испытаний - по мере формирования групп из числа лиц, подавших заявление о приеме и имеющих право на сдачу указанных испытаний в соответствии с утвержденным расписанием;
# публикация конкурсных списков - 22 августа;
# день завершения представления согласия на зачисление на основном этапе зачисления - 24 августа (представление согласия на зачисление осуществляется до 12:00 по московскому времени);
# издание приказа (приказов) о зачислении - 25 августа."""
# model = YandexGPT()
# print(
#     model.run(
#         "Расскажи мне о сроках проведения процедур приема и зачисления на обучение по программам магистратуры в 2025 году",
#         context_test,
#     ),
# )
