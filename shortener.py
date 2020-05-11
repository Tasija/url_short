"""Url Shortener based on base62 ids"""

from datetime import datetime

url_ids_pool = list(range(62, 3844))  # about 3780 url keys from 10 to ZZ
id_url_map = {}  # {"applau.se/df": ["applau.se/df", "full_url", url_id, 0, datetime.now()]

DOMAIN_NAME = "applau.se"


def id_encode(url_id):
    # base 62 characters
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = len(characters)
    ret = []
    # convert base10 id into base62 id for having alphanumeric shorten url
    while url_id > 0:
        val = url_id % base
        ret.append(characters[val])
        url_id = url_id // base
    # since ret has reversed order of base62 id, reverse ret before return it
    return "".join(ret[::-1])


def pop_lru_short_url():
    lru_short_url = sorted(
        id_url_map.values(), key=lambda x: x[-1], reverse=True).pop()
    del id_url_map[lru_short_url[0]]
    url_ids_pool.append(lru_short_url[2])


def get_short_url(full_url):
    """Genrate short url, add it to map"""
    try:
        url_id = url_ids_pool.pop()
    except (IndexError):
        # run out of short urls, reuse oldest
        pop_lru_short_url()
        url_id = url_ids_pool.pop()

    short_url = DOMAIN_NAME + "/" + id_encode(url_id)
    id_url_map[short_url] = [short_url, full_url, url_id, 0, datetime.now()]

    return short_url


def get_original_url(url_key):
    key = DOMAIN_NAME + "/" + url_key
    url_data = id_url_map.get(key)
    if url_data:
        # increment call count
        url_data[3] += 1
        # update call time
        url_data[-1] = datetime.now()

        return url_data[1]
