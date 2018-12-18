import psutil
from pip.utils import logging


def create_logger():
    logger = logging.getLogger("main")
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler("monitor.log")
    file_handler.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    formatter = logging.Formatter(
        "%(asctime)s [%(filename)s:%(lineno)s - %(funcName)s()] - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


def warn(name, value):
    logger.warning(
        "Beim Check {} mit dem Wert {} ist eine Warnung aufgetreten!".format(name, value))


def crit(name, value):
    logger.critical("Der Check {} mit dem Wert {} ist kritsch!".format(name, value))


def check(name, value, warning, critical):
    logger.debug('Der Wert {} wurde für diesen Check {} aktualisiert.'.format(value, name))
    if value > critical:
        crit(name, value)
    elif value > warning:
        warn(name, value)
    else:
        logger.info('Der Check {} ist im grünen Bereich.'.format(name))


# Erzeuge den Logger
logger = create_logger()

# Prüfe CPU
check("CPU", psutil.cpu_percent(), 50, 80)

# Prüfe Anzahl laufender Prozesse
prozesse = 0
for _ in psutil.process_iter():
    prozesse += 1
check("Prozesse", prozesse, 100, 200)
