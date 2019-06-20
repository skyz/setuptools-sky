from pkg_resources import iter_entry_points

from . import get_version
from .utils import do
from .version import _warn_if_setuptools_outdated


def version_keyword(dist, keyword, value):
    _warn_if_setuptools_outdated()
    if not value:
        return
    if value is True:
        value = {}
    if getattr(value, "__call__", None):
        value = value()

    dist.metadata.version = get_version(**value)


def find_files(path=""):
    for ep in iter_entry_points("setuptools_sky.files_command"):
        command = ep.load()
        if isinstance(command, str):
            # this technique is deprecated
            res = do(ep.load(), path or ".").splitlines()
        else:
            res = command(path)
        if res:
            return res
    return []
