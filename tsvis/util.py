from itertools import islice
from typing import Iterator, Dict, List


def chunk(it: Iterator, size: int) -> Iterator:
    """ Nice chunking method from: https://stackoverflow.com/a/22045226 """
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


def get_unique_elements(users: List[Dict], id_field: str = 'id') -> List[Dict]:
    """ Make list of dictionaries unique based on specified field with ID """
    return {u[id_field]: u for u in users}.values()
