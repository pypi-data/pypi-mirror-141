# coding=utf-8
# coding=utf-8
# signs pickled data to help ensure data integrity and security
# Based on https://pycharm-security.readthedocs.io/en/latest/checks/PIC100.html


import hashlib
import hmac
import io
import pickle
from contextlib import contextmanager
from importlib.resources import path as res_path, Resource, Package

from lz4 import frame as lz4f

PICKLE_KEY = b"fe95e0f8-b3d2-478d-88b2-c74b6e7194a4"
HASH_TYPE = hashlib.blake2b
HASH_LENGTH = 64


def dump(obj, file=None):
    if file is None:
        _file = io.BytesIO()
    else:
        _file = file
    with _maybe_open(_file, "wb") as fh:
        obj_pickle = pickle.dumps(obj, protocol=5)
        digest = hmac.new(PICKLE_KEY, obj_pickle, HASH_TYPE).digest()
        fh.write(digest)
        fh.write(lz4f.compress(obj_pickle))
    if file is None:
        return _file.getvalue()


def load(file):
    if isinstance(file, bytes):
        file = io.BytesIO(file)
    with _maybe_open(file, "rb") as fh:
        digest = fh.read(64)
        data = lz4f.decompress(fh.read())
        expected_digest = hmac.new(PICKLE_KEY, data, HASH_TYPE).digest()
        if not hmac.compare_digest(digest, expected_digest):
            raise ValueError(
                "pickled data digest does not match "
                "expected digest, did the file get corrupted or modified?"
            )
        # noinspection PickleLoad
        return pickle.loads(data)


def load_resource(package: Package, resource: Resource):
    with res_path(package, resource) as file:
        return load(file)


def save_resource(obj, package: Package, resource: Resource):
    with res_path(package, resource) as file:
        return dump(obj, file)


@contextmanager
def _maybe_open(file, *args, **kwargs):
    """
    Open the file if it's just a path, otherwise just yield
    :param file:
    :return:
    """
    if isinstance(file, io.IOBase):
        yield file
    else:
        with open(file, *args, **kwargs) as fh:
            yield fh
