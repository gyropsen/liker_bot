from dataclasses import dataclass

from environs import Env

from src.utils import get_channels, get_reactions


@dataclass
class Other:
    reactions: list[str]
    channels: list[str]


@dataclass
class UserBot:
    api_id: int
    api_hash: str


@dataclass
class Config:
    user_bot: UserBot
    other: Other


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        user_bot=UserBot(api_id=int(env("API_ID")), api_hash=env("API_HASH")),
        other=Other(reactions=get_reactions(), channels=get_channels()),
    )


config = load_config()
