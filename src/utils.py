import logging
import os
from pathlib import Path

import emoji

logger = logging.getLogger(__name__)


async def get_sessions_filenames(path: str = None) -> list[str, str] | list:
    """
    Поиск файлов по названию
    :param path: Путь к файлу
    :return: Список абсолютных путей к файлам сессий
    """
    if path is None:
        path = Path(Path(__file__).resolve().parent.parent, "sessions")
    accounts = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".session"):
                file = file.split(".")[0]
                accounts.append(Path(root, file))
    return accounts


async def delete_session(filename_session: str | Path) -> None:
    """
    Удаление файла сессии
    :param filename_session: Абсолютный путь к файлу сессии
    :return: None
    """
    os.remove(filename_session)


def get_reactions() -> list[str]:
    """
    Ввод списка эмодзи
    :return: список эмодзи
    """
    emoji_list = []
    while True:
        print("Добавленные эмодзи: ", emoji_list)
        reaction = input("Введите эмодзи или <q> для продолжения: ")
        if "q" == reaction:
            break
        elif ":" in emoji.demojize(reaction):
            emoji_list.append(reaction)
        else:
            print(f"Пожалуйста, введите эмодзи, не {reaction}")
    logger.info("Emojis: ", emoji_list)
    return emoji_list


def get_channels() -> list[str]:
    """
    Ввод списка каналов
    :return: список каналов
    """
    channel_list = []
    while True:
        print("Добавленные каналы: ", channel_list)
        channel = input("Введите канал или <q> для продолжения: ")
        if "q" == channel:
            break
        elif len(channel) >= 4:
            channel_list.append(channel)
        else:
            print(f"Пожалуйста, введите канал, не {channel}")
    logger.info("Channels: ", channel_list)
    return channel_list
