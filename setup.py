#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup

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
    version='0.5.1',
    packages=['afs'],
    package_dir={"": "src"},    
    setup_requires=['wheel'],
    description=DESCRIPTION,
    author='Juan Ignacio Rodríguez de León',
    author_email='euribates@gmail.com',
    url='https://github.com/euribates/agnostic-file-store/',
    download_url='https://github.com/euribates/agnostic-file-store/archive/master.zip',
    keywords=KEYWORDS,
    )
