"""\
important note:

the setup of setuptools_scm is self-using,
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
    egg_info = os.path.join(here, 'setuptools_scm.egg-info')
    has_entrypoints = os.path.isdir(egg_info)

    sys.path.insert(0, here)
    from setuptools_scm.hacks import parse_pkginfo
    from setuptools_scm.git import parse as parse_git
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
    install_requires=[
        'setuptools-scm>=1.5.4'
    ],
    setup_requires=[
        'setuptools-scm>=1.5.4'
    ],

    entry_points="""
        [distutils.setup_keywords]
        use_sky_version = setuptools_sky.integration:version_keyword

        [setuptools.file_finders]
        setuptools_scm = setuptools_scm.integration:find_files

        [setuptools_scm.parse_scm]
        .hg = setuptools_scm.hg:parse
        .git = setuptools_scm.git:parse

        [setuptools_scm.parse_scm_fallback]
        .hg_archival.txt = setuptools_scm.hg:parse_archival
        PKG-INFO = setuptools_scm.hacks:parse_pkginfo
        pip-egg-info = setuptools_scm.hacks:parse_pip_egg_info

        [setuptools_scm.files_command]
        .hg = setuptools_scm.hg:FILES_COMMAND
        .git = setuptools_scm.git:FILES_COMMAND

        [setuptools_scm.version_scheme]
        guess-next-dev = setuptools_sky.version:guess_next_dev_version
        post-release = setuptools_sky.version:postrelease_version

        [setuptools_scm.local_scheme]
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
