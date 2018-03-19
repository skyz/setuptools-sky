from __future__ import print_function
import sys
from setuptools_sky import get_version
from setuptools_sky.integration import find_files
from setuptools_sky.version import _warn_if_setuptools_outdated

if __name__ == '__main__':
    _warn_if_setuptools_outdated()
    print('Guessed Version', get_version())
    if 'ls' in sys.argv:
        for fname in find_files('.'):
            print(fname)
