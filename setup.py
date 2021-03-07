#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='agnostic-file-store',
    packages=['afs'],
    version='0.4.1',
    description='An agnostic, easy-to-use module for different file systems'
                  ' (At present just local an SMB)',
    author='Juan Ignacio Rodríguez de León',
    author_email='euribates@gmail.com',
    url='https://github.com/euribates/agnostic-file-store/',
    download_url='https://github.com/euribates/agnostic-file-store/archive/master.zip',
    long_description='README.md',
    long_description_content_type='markdown',
    keywords=['agnostic', 'SAN', 'NAS', 'Samba', 'SMB', 'CIFS'],
    classifiers= [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        ],
    )
