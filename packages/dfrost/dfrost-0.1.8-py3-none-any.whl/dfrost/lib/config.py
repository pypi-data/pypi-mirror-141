from os.path import expanduser
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern
from json import loads
from functools import cache


@cache
def get_dfrost_config():
    with open(expanduser("~/.dfrost.json")) as f:
        return loads(f.read())


def get_storage_bucket():
    return get_dfrost_config()["storage_bucket"]


def get_sync_dir():
    return get_dfrost_config()["sync_dir"]


@cache
def get_request_list():
    lines = get_dfrost_config().get("request_list", list())
    return PathSpec.from_lines(GitWildMatchPattern, lines)


@cache
def get_publish_list():
    lines = get_dfrost_config().get("publish_list", list())
    return PathSpec.from_lines(GitWildMatchPattern, lines)
