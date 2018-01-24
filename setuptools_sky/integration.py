from setuptools_scm import iter_matching_entrypoints

from . import get_version
from .version import _warn_if_setuptools_outdated


def version_keyword(dist, keyword, value):
    _warn_if_setuptools_outdated()
    if not value:
        return
    if value is True:
        value = {}
    if getattr(value, '__call__', None):
        value = value()
    # this piece of code is a hack to counter the mistake in root finding
    matching_fallbacks = iter_matching_entrypoints(
        '.', 'setuptools_scm.parse_scm_fallback')
    if any(matching_fallbacks):
        value.pop('root', None)
    dist.metadata.version = get_version(**value)
