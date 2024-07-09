import asyncio
import logging
import random

from pyrogram.types import Message

from src.account import TGPyrogramClient
from src.config import config

logger = logging.getLogger(__name__)


async def template_handler(client: TGPyrogramClient, message: Message) -> None:
    """
    Шаблон обработчика
    :param client: TGPyrogramClient
    :param message: Message
    :return:
    """
    digit = random.randint(0, 1)
    if digit == 0:
        timeout = random.randint(60, 1800)
        emoji = random.choice(config.other.reactions)
        logger.info(f"client: {client.name} will send reaction {emoji} in {timeout} seconds to {message.id}")
        await asyncio.sleep(timeout)
        await client.send_reaction(
            chat_id=message.chat.id, message_id=message.id, emoji=emoji
        )
        logger.info(f"Reaction {emoji} send in {timeout} seconds to {message.text[:15]}")
