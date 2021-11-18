import logging
from logging import handlers


def setup_log(name, filename, level='INFO'):
    log = logging.getLogger(name)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = handlers.RotatingFileHandler(filename, maxBytes=5_1000_1000, backupCount=3)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    log.addHandler(file_handler)
    log.addHandler(console_handler)
    log.setLevel(level)

    return log
