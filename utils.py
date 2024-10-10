import logging


def setup_logger(file_name, log_file):
    """Функция настройки логов для модулей"""

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(filename)s %(funcName)s %(levelname)s - %(message)s",
        filename=log_file,
        filemode="w",
        encoding="utf-8")
    logger = logging.getLogger(file_name)

    return logger