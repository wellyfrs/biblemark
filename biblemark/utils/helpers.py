from datetime import datetime
from multiprocessing import Manager

from biblemark.config.cache import get_cache

cache = get_cache()
manager = Manager()


def date(value: str) -> str:
    """Formats ISO datetime in a more human-readable text"""
    try:
        dt_object = datetime.fromisoformat(value)
        return dt_object.strftime("%B %d, %Y at %H:%M")
    except ValueError:
        return "Invalid date format"


def associate_by(items: iter, key: str) -> dict:
    """Associates items of an iterable in a dictionary with the chosen item property as key"""
    items_by_key = {item[key]: item for item in items}
    return items_by_key
