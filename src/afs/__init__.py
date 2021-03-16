#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# AFS - Agnostic File Storage

The purpose of this module is to offer an agnostic, easy-to-use module
for different file systems (At present time, just local and SMB/CIFS).
The initial use of this module was provide an easy path to translate
local file systems operations to a network samba server.

## Example of use

So, you can translate code like this:

    if os.path.isdir('/tmp/token.txt'):
        if not os.path.isdir('/tmp/results'):
            os.mkdir('/tmp/results')
        with open('/tmp/results/data.txt', 'wb') as f:
            f.write('This is an example\n')

To something like this (which must work identical):

    with afs.connect('temp') as fs:
        if not fs.isdir('results'):
            fs.mkdir('results')
        fs.cd('results')
        fs.save('data.txt', 'This is an example\n')

The entry `temp` is defined in a configuration file, using a format
similar to windows .INI files, like this:

    [temp]
    kind: local
    base: /tmp

We can now switch to another directory by just replacing the `temp` base
entry to the desired base path, for example. More interesting, you can
change to a network SMB Server, modifying the configuration file to:

    [temp]
    kind: smb
    username: samba_user
    password: samba_password
    host: nas
    domain: mycompany.com
    service: test$
"""

__version__ = '0.4.2'

import os

from six.moves import configparser

from . import errors
from .afs_memory import MemoryFileStorage
from .afs_smb import SMBFileStorage
from .afs_local import LocalFileStorage


_first_option_filename = ''


def get_options_filename():
    global _first_option_filename
    if _first_option_filename:
        yield(_first_option_filename)
    src = 'afs.ini'
    yield os.path.join('/etc', src)
    yield os.path.join(os.path.expanduser('~'), src)
    module_dir = os.path.dirname(os.path.abspath(__file__))
    yield os.path.join(module_dir, src)


def set_options_filename(fn):
    global _first_option_filename
    if os.path.isfile(fn):
        _first_option_filename = fn


class Sources(object):

    config_files = []
    _sources = {}
    singleton = None
    initialized = False

    def __new__(cls, config_fn=''):  # __new__ always a classmethod
        if not Sources.initialized:
            Sources.singleton = object.__new__(cls)
            config = configparser.ConfigParser()
            for fn in get_options_filename():
                if os.path.isfile(fn):
                    Sources.singleton.read_configuration(fn)
            Sources.initialized = True
        if config_fn and config_fn not in Sources.config_files:
            Sources.singleton.read_configuration(config_fn)
        if not Sources._sources:
            raise errors.configuration_not_found()
        return Sources.singleton

    def add_source(self, name, afs):
        Sources._sources[name] = afs

    def get_sources(self):
        return Sources._sources.keys()

    def get_source(self, name):
        if name not in Sources._sources:
            raise ValueError(
                "Can't connect to {n}\n"
                "Configuration files: {f}."
                .format(n=name, f=', '.join(self.config_files))
                )
        result = Sources._sources.get(name)
        return result

    def read_configuration(self, config_fn):
        self.config_files.append(config_fn)
        config = configparser.ConfigParser()
        config.read(config_fn)
        for name in config.sections():
            args = dict(config.items(name))
            kind = args.pop('kind')
            if kind == 'smb':
                self.add_source(name, SMBFileStorage(name, **args))
            elif kind == 'local':
                self.add_source(name, LocalFileStorage(name, **args))
            else:
                raise ValueError(
                    "Don't know how to handle this kind "
                    "of file storage service: {k}.\n"
                    "Configuration file is {f}."
                    .format(k=kind, f=self.configuration_file)
                    )


def connect(name, config_fn=''):
    if config_fn == ':memory:':
        return MemoryFileStorage()
    else:
        sources = Sources(config_fn)
        return sources.get_source(name)
