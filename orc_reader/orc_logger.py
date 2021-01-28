from logging import DEBUG, Formatter, StreamHandler, basicConfig, getLogger

logger = getLogger(__name__)
logger.setLevel(DEBUG)

ch = StreamHandler()
ch.setLevel(DEBUG)
formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def set_log_name(log_name='info.log'):
    basicConfig(
        filename=log_name,
        level=DEBUG,
    )


def info(message):
    logger.info(message)


def error(message):
    logger.error(message)
