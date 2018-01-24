from __future__ import print_function

import os
import re
import warnings
from distutils import log

from setuptools_scm import trace
from setuptools_scm.version import callable_or_entrypoint

try:
    from pkg_resources import parse_version, SetuptoolsVersion
except ImportError as e:
    parse_version = SetuptoolsVersion = None


def _warn_if_setuptools_outdated():
    if parse_version is None:
        log.warn("your setuptools is too old (<12)")
        log.warn("setuptools_scm functionality is degraded")


def tag_to_version(tag):
    trace('tag', tag)
    if '+' in tag:
        warnings.warn("tag %r will be stripped of the local component" % tag)
        tag = tag.split('+')[0]
    # lstrip the v because of py2/py3 differences in setuptools
    # also required for old versions of setuptools

    version = tag.rsplit('-', 1)[-1].lstrip('v')
    if parse_version is None:
        return version
    version = parse_version(version)
    trace('version', repr(version))
    if isinstance(version, SetuptoolsVersion):
        return version


def tags_to_versions(tags):
    versions = map(tag_to_version, tags)
    return [v for v in versions if v is not None]


def _parse_tag(tag, preformatted):
    if preformatted:
        return tag
    if SetuptoolsVersion is None or not isinstance(tag, SetuptoolsVersion):
        tag = tag_to_version(tag)
    return tag


def guess_next_version(tag_version, distance):
    version = _strip_local(str(tag_version))
    bumped = _bump_dev(version) or _bump_regex(version)
    suffix = '.dev%s' % distance
    return bumped + suffix


def _strip_local(version_string):
    public, sep, local = version_string.partition('+')
    return public


def _bump_dev(version):
    if '.dev' not in version:
        return

    prefix, tail = version.rsplit('.dev', 1)
    assert tail == '0', 'own dev numbers are unsupported'
    return prefix


def _bump_regex(version):
    prefix, tail = re.match('(.*?)(\d+)$', version).groups()
    return '%s%d' % (prefix, int(tail) + 1)


def guess_next_dev_version(version):
    if version.exact:
        return version.format_with("{tag}")
    else:
        branch_name = os.environ.get('BRANCH_NAME', "develop")

        if branch_name.startswith('PR'):
            target_branch = os.environ.get('CHANGE_TARGET', 'develop')

            if target_branch.startswith('master'):
                return '%s.%s' % (version.tag.base_version, version.format_with('rc{distance}'))
            elif target_branch.startswith('develop'):
                return '%s.%s' % (version.tag.base_version, version.format_with('beta{distance}'))
        elif branch_name.startswith('master'):
            return version.tag.base_version
        elif branch_name.startswith('release'):
            return '%s.%s' % (version.tag.base_version, version.format_with('rc.{distance}'))
        elif branch_name.startswith('develop'):
            return '%s.%s' % (version.tag.base_version, version.format_with('beta.{distance}'))
        else:
            return '%s.%s' % (version.tag.base_version, version.format_with('alpha.{distance}'))


def get_local_node_and_date(version):
    return ''
    # if version.exact or version.node is None:
    #     return version.format_choice("", "+d{time:%Y%m%d}")
    # else:
    #     return version.format_choice("+{node}", "+{node}.d{time:%Y%m%d}")


def get_local_dirty_tag(version):
    return version.format_choice('', '+dirty')


def postrelease_version(version):
    if version.exact:
        return version.format_with('{tag}')
    else:
        return version.format_with('{tag}.post{distance}')


def format_version(version, **config):
    trace('sky version', version)
    trace('config', config)
    if version.preformatted:
        return version.tag
    version_scheme = callable_or_entrypoint(
        'setuptools_sky.version_scheme', config['version_scheme'])
    local_scheme = callable_or_entrypoint(
        'setuptools_sky.local_scheme', config['local_scheme'])
    main_version = version_scheme(version)
    trace('version', main_version)
    local_version = local_scheme(version)
    trace('local_version', local_version)
    return version_scheme(version) + local_scheme(version)
