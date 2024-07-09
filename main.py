import asyncio

from pyrogram import compose, filters
from pyrogram.handlers import MessageHandler

from src.account import TGPyrogramClient
from src.config import config
from src.handlers import template_handler
from src.logger import setup_logging


async def main():
    """
    Главная функция
    """

    # Настроить логгирование
    logger = setup_logging()

    # Создать клиентов на основе файлов сессий
    clients: list[TGPyrogramClient] = await TGPyrogramClient.get_clients()

    # Проверить работоспособность клиентов
    for client in clients:
        await client.check_session()
    logger.info("All accounts is available")

    # Найти каналы
    channels = await clients[0].search_channel(config.other.channels)

    # Подписаться на каналы
    # Это нужно для того, чтобы аккаунты могли получать обновления из чатов,
    # их отслеживать и автоматически проставлять реакции
    for client in clients:
        for channel in channels:
            await client.subscribe(channel)
    logger.info("All accounts subscribed to the channels")

    # Регистрация обработчиков
    handlers = [MessageHandler(template_handler, filters.chat(channel.id)) for channel in channels]
    for client in clients:
        for handler in handlers:
            client.add_handler(handler)

    logger.info("Started!")
    # Запустить клиентов
    await compose(clients)


if __name__ == "__main__":
    asyncio.run(main())
