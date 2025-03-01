from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv(override=True)


@dataclass
class BotConfig:
    token: str = getenv("BOT_TOKEN")


@dataclass
class LLMConfig:
    token: str = getenv("LLM_TOKEN")
    folder_id: str = getenv("LLM_FOLDER_ID")


@dataclass
class VKConfig:
    token: str = getenv("VK_TOKEN")
    group_id: str = getenv("VK_GROUP_ID")
    owner_id: str = getenv("VK_OWNER_ID")
    group_domain: str = getenv("VK_GROUP_DOMAIN")


@dataclass
class Configuration:
    bot = BotConfig()
    vk = VKConfig()
    llm = LLMConfig()


cfg = Configuration()
