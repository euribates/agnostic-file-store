#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import functools
import os
from . import log

from .core import AFSFile, AFSDirectory, AFSListing, AgnosticFileStorage
from .exceptions import AgnosticFileStorageError

LOG_LEVEL = log.INFO
logger = log.get_logger(__name__, LOG_LEVEL)

class LocalFileStorage(AgnosticFileStorage):

    def __init__(self, name, **kwargs):
        super(LocalFileStorage, self).__init__(name)
        self.base = self.get_value(kwargs, 'base')
        self.is_connected = False

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

    def open(self):
        self.is_connected = True 
        return self

    def close(self):
        self.is_connected = False

    def is_dir(self, path):
        full_path = self.get_local_path(path)
        return os.path.isdir(full_path)

    def is_file(self, path):
        full_path = self.get_local_path(path)
        return os.path.isfile(full_path)

    def ls(self):
        logger.debug('Calling method ls in LocalFileStorage("{}")'.format(self.name))
        if self.is_connected:
            result = AFSListing()
            for filename in os.listdir(self.get_local_path()):
                full_path = self.get_local_path(filename)
                if os.path.isfile(full_path):
                    result.append(AFSFile(filename, os.path.getsize(full_path)))
                else:
                    result.append(AFSDirectory(filename, 0))
            return result
        else:
            raise AgnosticFileStorageError('No connection')

    #@log.trace(logger)
    def save(self, filename, stream):
        if self.is_connected:
            full_path = self.get_local_path(filename)
            buff = stream.read()
            size = len(buff)
            with open(full_path, 'wb') as f:
                f.write(buff)
            return size
        else:
            raise AgnosticFileStorageError('No connection')

    def mkdir(self, dir_name):
        logger.debug('Calling method mkdir("{}") in LocalFileStorage("{}")'.format(
            dir_name, 
            self.name,
            ))
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
        logger.debug('Calling method rmdir("{}") in LocalFileStorage("{}")'.format(
            dir_name, 
            self.name,
            ))
        if self.is_connected:
            if self.is_dir(dir_name):
                full_path = self.get_local_path(dir_name)
                os.rmdir(full_path)
                return True
            else:
                return False
        else:
            raise AgnosticFileStorageError('No connection')

    def rm(self, file_name):
        logger.debug('Calling method rm("{}") in LocalFileStorage("{}")'.format(
            file_name, 
            self.name,
            ))
        if self.is_connected:
            if self.is_file(file_name):
                full_path = self.get_local_path(file_name)
                os.unlink(full_path)
                return True
            elif self.is_dir(file_name):
                raise AgnosticFileStorageError(
                    'Can\'t delete a directory with method rm().\n'
                    'Use the rmdir() method'
                    )
            else:
                return False
        else:
            raise AgnosticFileStorageError('No conecttion')


