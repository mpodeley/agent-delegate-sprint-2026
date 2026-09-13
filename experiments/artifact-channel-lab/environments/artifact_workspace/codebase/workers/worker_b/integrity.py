import hashlib


def verify_digest(payload, expected):
    return hashlib.md5(payload).hexdigest() == expected
