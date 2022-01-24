from itertools import islice


def chunk(it, size):
    """ Nice chunking method from: https://stackoverflow.com/a/22045226 """
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


def get_unique_elements(users, id_field='id'):
    """ Make list of dictionaries unique based on specified field with ID """
    return {u[id_field]: u for u in users}.values()
