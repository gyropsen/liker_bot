import logging
from datetime import datetime
from pathlib import Path
from typing import Any


def setup_logging() -> Any:
    """
    Функция логгирования
    :return: Логгер
    """
    for name, logger in logging.root.manager.loggerDict.items():
        if name.startswith("pyrogram"):
            if isinstance(logger, logging.Logger):
                logger.setLevel(logging.WARNING)

    logger = logging.getLogger()

    file_handler = logging.FileHandler(
        str(Path(Path(__file__).resolve().parent.parent, "logs", f"{datetime.now().date()}_logs.log")), "w"
    )
    console_handler = logging.StreamHandler()

    file_formatter = logging.Formatter("%(asctime)s %(name)s %(funcName)s %(levelname)s: %(message)s")
    console_formatter = logging.Formatter("%(asctime)s %(name)s %(funcName)s %(levelname)s: %(message)s")

    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.setLevel(logging.INFO)
    return logger
