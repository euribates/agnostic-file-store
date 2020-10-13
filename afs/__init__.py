#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import logging
from six.moves import configparser

from .exceptions import AgnosticFileStorageError
from .core import AFSFile, AFSDirectory, AFSListing
from .afs_smb import SMBFileStorage
from .afs_local import LocalFileStorage


_first_option_filename = ''


from .exceptions import AgnosticFileStorageError, ConfigurationFileNotFound


def get_options_filename():
    global _first_option_filename
    if _first_option_filename:
        yiend(_first_option_filename)
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

    def __new__(cls, config_fn=''): # __new__ always a classmethod
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
            raise ConfigurationFileNotFound()
        return Sources.singleton

    def add_source(self, name, afs):
        Sources._sources[name] = afs

    def get_sources(self):
        return Sources._sources.keys()

    def get_source(self, name):
        if name not in Sources._sources:
            raise AgnosticFileStorageError(
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
                raise AgnosticFileStorageError(
                    "Don't know how to handle this kind "
                    "of file storage service: {k}.\n"
                    "Configuration file is {f}."
                    .format(k=kind, f=self.configuration_file)
                    )


def connect(name, config_fn=''):
    sources = Sources(config_fn)
    return sources.get_source(name)


