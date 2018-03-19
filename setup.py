"""\
important note:

the setup of setuptools_sky is self-using,
the first execution of `python setup.py egg_info`
will generate partial data
its critical to run `python setup.py egg_info`
once before running sdist or easy_install on a fresh checkouts

pip usage is recommended
"""
from __future__ import print_function

import setuptools

with open('README.rst') as fp:
    long_description = fp.read()


def scm_config():
    import os
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    egg_info = os.path.join(here, 'setuptools_sky.egg-info')
    has_entrypoints = os.path.isdir(egg_info)

    sys.path.insert(0, here)
    from setuptools_sky.hacks import parse_pkginfo
    from setuptools_sky.git import parse as parse_git
    from setuptools_sky.version import (

        guess_next_dev_version,
        get_local_node_and_date,
    )

    def parse(root):
        try:
            return parse_pkginfo(root)
        except IOError:
            return parse_git(root)

    config = dict(
        version_scheme=guess_next_dev_version,
        local_scheme=get_local_node_and_date,
    )

    if has_entrypoints:
        return dict(use_sky_version=config)
    else:
        from setuptools_sky import get_version
        return dict(version=get_version(
            root=here, parse=parse, **config))


arguments = dict(
    name='setuptools_sky',
    url='https://bitbucket.org/sekomy/setuptools-sky',
    author='Sekom Yazilim',
    author_email='info@sekomyazilim.com.tr',
    license='MIT',
    description='the blessed package to manage your versions by scm tags',
    zip_safe=True,
    long_description=long_description,

    packages=[
        'setuptools_sky',
    ],
    entry_points="""
        [distutils.setup_keywords]
        use_sky_version = setuptools_sky.integration:version_keyword

        [setuptools.file_finders]
        setuptools_sky = setuptools_sky.integration:find_files

        [setuptools_sky.parse_scm]
        .hg = setuptools_sky.hg:parse
        .git = setuptools_sky.git:parse

        [setuptools_sky.parse_scm_fallback]
        .hg_archival.txt = setuptools_sky.hg:parse_archival
        PKG-INFO = setuptools_sky.hacks:parse_pkginfo
        pip-egg-info = setuptools_sky.hacks:parse_pip_egg_info

        [setuptools_sky.files_command]
        .hg = setuptools_sky.hg:FILES_COMMAND
        .git = setuptools_sky.git:FILES_COMMAND

        [setuptools_sky.version_scheme]
        guess-next-dev = setuptools_sky.version:guess_next_dev_version
        post-release = setuptools_sky.version:postrelease_version

        [setuptools_sky.local_scheme]
        node-and-date = setuptools_sky.version:get_local_node_and_date
        dirty-tag = setuptools_sky.version:get_local_dirty_tag
    """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Version Control',
        'Topic :: System :: Software Distribution',
        'Topic :: Utilities',
    ],
)

if __name__ == '__main__':
    arguments.update(scm_config())
    setuptools.setup(**arguments)
