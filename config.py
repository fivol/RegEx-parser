REGEX_ALPHABET = set('abc')

# Logger staff
import logging


logger = logging.getLogger("main_logger")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()

formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add handler to logger object
logger.addHandler(handler)
