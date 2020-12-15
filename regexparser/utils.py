import functools
from operator import or_


def merge_sets(sets_list):
    return functools.reduce(or_, sets_list, set())
