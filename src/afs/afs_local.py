#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os

from . import errors
from . import log
from .core import AFSFile, AFSDirectory, AFSListing, AgnosticFileStorage
from .exceptions import AgnosticFileStorageError


LOG_LEVEL = log.INFO
logger = log.get_logger(__name__, LOG_LEVEL)


class LocalFileStorage(AgnosticFileStorage):

    def __init__(self, name, **kwargs):
        super(LocalFileStorage, self).__init__(name)
        self.base = self.get_value(kwargs, 'base')

    def get_local_path(self, filename=''):
        path = [self.base]
        path.extend(self.cwd())
        if filename:
            path.append(filename)
        return os.path.sep.join(path)

    def __str__(self):
        bar = '-' * (59 - len(self.name))
        buff = ['--[ LocalFileStorage {} ]{}'.format(self.name, bar)]
        buff.append('base: {}'.format(self.base))
        buff.append('-'*80)
        return '\n'.join(buff)

    def is_dir(self, path):
        full_path = self.get_local_path(path)
        return os.path.isdir(full_path)

    def is_file(self, path):
        full_path = self.get_local_path(path)
        return os.path.isfile(full_path)

    def ls(self):
        logger.debug('LocalFileStorage::ls(%r)', self.name)
        if not self.is_connected:
            raise errors.no_conexion()
        result = AFSListing()
        for filename in os.listdir(self.get_local_path()):
            full_path = self.get_local_path(filename)
            if os.path.isfile(full_path):
                result.append(AFSFile(filename, os.path.getsize(full_path)))
            else:
                result.append(AFSDirectory(filename, 0))
        return result

    def save(self, filename, stream):
        logger.debug('LocalFileStore::save(%r, %s)', filename, stream)
        if not self.is_connected:
            raise errors.no_conexion()
        full_path = self.get_local_path(filename)
        buff = stream.read()
        size = len(buff)
        mode = 'wb' if isinstance(buff, bytes) else 'w'
        with open(full_path, mode) as _f:
            _f.write(buff)
        return size

    def mkdir(self, dir_name):
        logger.debug('LocalFileStore::mkdir(%r)', dir_name)
        if not self.is_connected:
            raise errors.no_conexion()
        if self.is_connected:
            if not self.is_dir(dir_name):
                full_path = self.get_local_path(dir_name)
                os.mkdir(full_path)
                return True
            else:
                return False
        else:
            raise AgnosticFileStorageError('No connection')

    def rmdir(self, dir_name):
        logger.debug('LocalFileStore::rmdir(%r)', dir_name)
        if not self.is_connected:
            raise errors.no_conexion()
        if self.is_dir(dir_name):
            full_path = self.get_local_path(dir_name)
            os.rmdir(full_path)
            return True
        return False

    def rm(self, file_name):
        logger.debug('LocalFileStore::rm(%r)', file_name)
        if not self.is_connected:
            raise errors.no_conexion()
        if self.is_dir(file_name):
            raise errors.can_not_delete_directory(file_name)
        if self.is_file(file_name):
            full_path = self.get_local_path(file_name)
            os.unlink(full_path)
            return True
        return False
