import functools
from operator import or_

from regexparser.config import logger


def func_logger(func):
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        try:
            logger.debug("{0} - {1} - {2}".format(func.__name__, args, kwargs))
            result = func(*args, **kwargs)
            logger.debug(result)
            return result
        except Exception as ex:
            logger.debug("Exception {0}".format(ex))
            raise ex

    return decorated


def merge_sets(sets_list):
    return functools.reduce(or_, sets_list, set())
