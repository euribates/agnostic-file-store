#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from . import log
import os


logger = log.get_logger(__name__)


class AFSEntry(object):

    def __init__(self, filename, size):
        self.name = filename
        self.size = size


class AFSFile(AFSEntry):

    def is_dir(self):
        return False

    def is_file(self):
        return True

    def __str__(self):
        return self.name


class AFSDirectory(AFSEntry):

    def is_dir(self):
        return True

    def is_file(self):
        return False

    def __str__(self):
        return '{}/'.format(self.name)


class AFSListing(list):

    def index(self, item):
        return [_.name for _ in self].index(item)

    def __contains__(self, item):
        return item in [_.name for _ in self]


class AgnosticFileStorage(object):

    def __init__(self, name):
        self.name = name
        self.current_dir = []
        self.is_connected = False

    def open(self):
        super(AgnosticFileStorage, self).__init__()
        self.is_connected = True
        return self

    def close(self):
        self.is_connected = False

    def __del__(self):
        self.close()

    def __enter__(self):
        self.current_dir = []
        return self.open()

    def __exit__(self, _type, value, traceback):
        self.close()

    def cwd(self):
        return self.current_dir[:]

    def get_absolute_path(self, file_name, sep='/'):
        if self.current_dir:
            base = sep.join(self.cwd())
            return '{base}{sep}{fn}'.format(
                base=base,
                sep=sep, 
                fn=file_name,
                )
        else:
            return '{sep}{fn}'.format(
                sep=sep,
                fn=file_name,
                )

    def cd(self, path):
        if not self.is_dir(path):
            raise ValueError(
                'Can\'t change directory.\n'
                'The suplied path [{}] doesn\'t exits or '
                'is a regular file.\n'.format(path)
                )
        self.current_dir.append(path)

    def get_value(self, dict, name, default=None):
        value = dict.get(name, default)
        if value and value.startswith('%') and value.endswith('%'):
            env_entry = value[1:-1]
            return os.environ.get(env_entry, default)
        else:
            return value

    def set_path(self, *dirs, **kwargs):
        create = kwargs.pop('create', True)
        for dir in dirs:
            if not self.is_dir(dir):
                if create:
                    self.mkdir(dir)
                else:
                    return False
            self.cd(dir)
        return True
