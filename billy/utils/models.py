from __future__ import unicode_literals

import random
import uuid

from sqlalchemy import Enum

ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class Enum(Enum):
    """
    Better sqlalchemy enum with a getattr
    """
    def __getattr__(self, item):
        if item in self.enums:
            return item
        raise ValueError('{} not set.'.format(item))



def base62_encode(num, alphabet=ALPHABET):
    """Encode a number in Base X

    `num`: The number to encode
    `alphabet`: The alphabet to use for encoding
    """
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


def uuid_factory(prefix=None):
    """
    Given a prefix, which defaults to None, will generate a function
    which when called, will generate a hex uuid string using uuid.uuid1()

    If a prefix string is passed, it prefixes the uuid.
    """

    def generate_uuid():
        the_uuid = base62_encode(uuid.uuid1().int)
        if prefix:
            the_uuid = prefix + the_uuid

        return the_uuid

    return generate_uuid


def api_key_factory():
    """
    TODO: Marsenne twister is predictable. Up the security
    """

    generator = lambda: ''.join([random.choice(ALPHABET) for _ in xrange(32)])
    return generator


