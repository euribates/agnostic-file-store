#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from setuptools import setup


def get_version():
    """Get the current version of the package.

    We parse the file in order to not execute the code.
    """
    pat_version = re.compile(r"__version__\s*=\s*['\"](.+)['\"]")
    version_file = "src/afs/__init__.py"
    with open(version_file) as f:
        for line in f:
            m = pat_version.match(line)
            if m:
                return m.group(1)
    raise ValueError("AFS: setup.py can't read the version number")


KEYWORDS = [
    'agnostic',
    'AMS',
    'CIFS',
    'NAS',
    'S3',
    'Samba',
    'SAN',
    'SMB',
    'storage',
]

DESCRIPTION = (
    'An agnostic, easy-to-use module for different file systems'
    ' (Memory | local | Samba (SMB) | NFS | Amazon S3)'
)

setup(
    name='agnostic-file-store',
    version=get_version(),
    packages=['afs'],
    package_dir={"": "src"},    
    setup_requires=['wheel'],
    install_requires=['pysmb'],
    description=DESCRIPTION,
    author='Juan Ignacio Rodríguez de León',
    author_email='euribates@gmail.com',
    url='https://github.com/euribates/agnostic-file-store/',
    download_url='https://github.com/euribates/agnostic-file-store/archive/master.zip',
    keywords=KEYWORDS,
    )
