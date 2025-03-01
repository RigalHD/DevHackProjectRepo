from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv()


@dataclass
class BotConfig:
    token: str = getenv("BOT_TOKEN")


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


cfg = Configuration()
