#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# AFS - Agnostic File Storage

The purpose of this module is to offer an agnostic, easy-to-use module
for different file systems (At present time, just local and SMB/CIFS).
The initial use of this module was provide an easy path to translate
local file systems operations to a network samba server.
"""

__version__ = '0.5.4'

import os

from six.moves import configparser

from . import errors
from .afs_local import LocalFileStorage
from .afs_memory import MemoryFileStorage
from .afs_sftp import SFTPFileStorage
from .afs_smb import SMBFileStorage


KIND_MAP = {
    'local': LocalFileStorage,
    'memory': MemoryFileStorage,
    'sftp': SFTPFileStorage,
    'smb': SMBFileStorage,
}

config_file = None

sources = {}


def search_options_filename(filename=None):
    src = 'afs.ini'
    yield os.path.join('/etc', src)
    yield os.path.join(os.path.expanduser('~'), src)
    local_dir = os.path.dirname(os.path.abspath(__file__))
    for _ in range(local_dir.count(os.path.sep)):
        yield os.path.join(local_dir, src)
        local_dir = os.path.dirname(local_dir)


def add_source(name, params):
    kind = params.pop('kind')
    if kind in KIND_MAP:
        StorageKlass = KIND_MAP[kind]  # NOQA
        sources[name] = StorageKlass(name, **params)
    else:
        raise errors.config_file_not_found(kind, config_file)


def read_configuration():
    global config_file
    for filename in search_options_filename():
        if os.path.isfile(filename):
            config_file = filename
            config = configparser.ConfigParser()
            config.read(filename)
            for name in config.sections():
                args = dict(config.items(name))
                add_source(name, args)
            return sources


def connect(name):
    global sources
    if not sources:
        read_configuration()
    return sources[name]
