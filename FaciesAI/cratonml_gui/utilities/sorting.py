import logging
import re

COMPILED = re.compile(r"([А-Я|A-Z ]+)([0-9]+)", re.I)
logger = logging.getLogger("__name__")


def sort_key(item: str) -> tuple[str, int]:
    match = COMPILED.match(item)
    return match[1], int(match[2])


def sort(data):
    try:
        data = sorted(data, key=sort_key)
    except Exception as e:
        logger.error(e, exc_info=True)
        data.sort()
    return data
