import logging

from pyrogram import Client
from pyrogram.raw.types import Channel

from src.config import config
from src.utils import delete_session, get_sessions_filenames

logger = logging.getLogger(__name__)


class TGPyrogramClient(Client):
    channel = []

    def __init__(self, *args, name, **kwargs):
        super().__init__(*args, name, **kwargs)

    async def check_session(self) -> None:
        """
        Проверка авторизации и других ошибок в сессии
        """
        try:
            async with self:
                await self.get_me()
                logger.info(f"Account, {self.name} is available")
        except Exception as e:
            logger.error(f"Account, {self.name} is not available: {e}, removing from list, deleting session")
            await delete_session(self.name + ".session")

    @classmethod
    async def get_clients(cls) -> list:
        """
        Фабрика клиентов
        :return: Список клиентов
        """
        return [
            TGPyrogramClient(
                name=str(filename_session), api_id=config.user_bot.api_id, api_hash=config.user_bot.api_hash
            )
            for filename_session in await get_sessions_filenames()
        ]

    async def search_channel(self, channels_names: list[str]) -> list:
        channels = []
        async with self:
            for channel in channels_names:
                try:
                    channel = await self.get_chat(channel)
                    if channel:
                        channels.append(channel)
                    else:
                        logger.error(f"Channel {channel} not found")
                except Exception as e:
                    logger.error(f"Channel {channel} not found: {e}")
        return channels

    async def check_subscribe(self, channel: Channel) -> bool:
        """
        Проверяет, подписан ли аккаунт на канал
        :param channel: telegram канал
        :return: True - если, аккаунт подписан, False - если нет
        """
        async for dialog in self.get_dialogs():
            if dialog.chat.username:
                if str(dialog.chat.username).lower() == str(channel.username).lower():
                    return True
        return False

    async def subscribe(self, channel: Channel) -> None:
        """
        Подписаться аккаунтом на канал
        :param channel: telegram канал
        :return: None
        """
        async with self:
            sub = await self.check_subscribe(channel)
            if sub:
                logger.info(f"Account {self.name} was subscribed to the channel {channel.username}")
            else:
                await self.join_chat(chat_id=channel.username)
                logger.info(f"Account {self.name} subscribed to the channel {channel.username}")
