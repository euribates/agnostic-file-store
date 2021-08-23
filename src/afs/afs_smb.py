#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import socket

from smb.SMBConnection import SMBConnection
from smb.smb_structs import OperationFailure

from .core import AFSFile, AFSDirectory, AFSListing, AgnosticFileStorage
from .exceptions import AgnosticFileStorageError
from . import log


NUM_RETRIES = 15


LOG_LEVEL = log.INFO
logger = log.get_logger(__name__, LOG_LEVEL)


class SMBFileStorage(AgnosticFileStorage):

    def __init__(self, name, **kwargs):
        super(SMBFileStorage, self).__init__(name)
        self.username = self.get_value(kwargs, 'username')
        self.password = self.get_value(kwargs, 'password')
        self.host = self.get_value(kwargs, 'host')
        self.client = socket.gethostname()
        self.domain = self.get_value(kwargs, 'domain')
        self.service = self.get_value(kwargs, 'service')
        self.is_connected = False
        import logging; logging.error("self.fqn is %s", self.fqn)

    @property
    def fqn(self):
        if self.domain:
            return '{}.{}'.format(self.domain, self.name)
        else:
            return self.host

    def __repr__(self):
        buff = [f'SMBFileStorage({self.name}']
        buff.append('username={self.username!repr}')
        buff.append('host={self.host!repr}')
        buff.append('host={self.host!repr}')
        buff.append('domain={self.domain!repr}')
        buff.append('service={self.service!repr})')
        return ', '.join(buff)

    def open(self):
        import logging; logging.error("self is %r (%s)", self, type(self))
        self.conn = SMBConnection(
            self.username,
            self.password,
            self.client,
            self.host,
            self.domain,
            use_ntlm_v2=False,
            sign_options=SMBConnection.SIGN_NEVER,
            is_direct_tcp=True,
            )
        self.is_connected = self.conn.connect(self.fqn, 445)
        super(SMBFileStorage, self).open()
        return self

    def close(self):
        if self.is_connected:
            self.conn.close()
        super(SMBFileStorage, self).close()

    def is_dir(self, path):
        full_path = self.get_absolute_path(path)
        try:
            attr = self.conn.getAttributes(self.service, full_path, timeout=30)
            return attr.isDirectory
        except OperationFailure:
            return False

    def is_file(self, path):
        full_path = self.get_absolute_path(path)
        try:
            attr = self.conn.getAttributes(self.service, full_path, timeout=30)
            return not attr.isDirectory
        except OperationFailure:
            return False

    def ls(self):
        logger.info('Call method ls in SMBFileStorage("%s")', self.name)
        tries = 0
        if self.is_connected:
            while tries < NUM_RETRIES:
                try:
                    result = AFSListing()
                    path = '/'.join(self.cwd())
                    for f in self.conn.listPath(self.service, path):
                        if f.isDirectory:
                            result.append(AFSDirectory(f.filename, f.file_size))
                        else:
                            result.append(AFSFile(f.filename, f.file_size))
                    return result
                except Exception as err:
                    pass
                finally:
                    tries += 1
            raise AgnosticFileStorageError(
                "Can't read the content of {}".format(self.cwd())
                )
        else:
            raise AgnosticFileStorageError('No connection')

    # @log.trace(logger)
    def save(self, filename, stream):
        if self.is_connected:
            full_path = self.get_absolute_path(filename)
            bytes_stored = self.conn.storeFile(self.service, full_path, stream)
            return bytes_stored
        else:
            raise AgnosticFileStorageError('No connection')

    def mkdir(self, dir_name):
        logger.debug('Calling method mkdir("{}") in SMBFileStorage("{}")'.format(
            dir_name,
            self.name,
            ))
        if self.is_connected:
            if not self.is_dir(dir_name):
                full_path = self.get_absolute_path(dir_name)
                self.conn.createDirectory(self.service, full_path)
                return True
            else:
                return False
        else:
            raise AgnosticFileStorageError('No connection')

    def rmdir(self, dir_name):
        logger.debug('Calling method rmdir("{}") in SMBFileStorage("{}")'.format(
            dir_name,
            self.name,
            ))
        if self.is_connected:
            if self.is_dir(dir_name):
                full_path = self.get_absolute_path(dir_name)
                self.conn.deleteDirectory(self.service, full_path)
                return True
            else:
                return False
        else:
            raise AgnosticFileStorageError('No connection')

    def rm(self, file_name):
        logger.debug('Calling method rm("{}") in SMBFileStorage("{}")'.format(
            file_name,
            self.name,
            ))
        if self.is_connected:
            if self.is_file(file_name):
                full_path = self.get_absolute_path(file_name)
                self.conn.deleteFiles(self.service, full_path)
                return True
            elif self.is_dir(file_name):
                raise AgnosticFileStorageError(
                    "Can't delete a directory with method rm().\n"
                    "Use the rmdir() method"
                    )
            else:
                return False
        else:
            raise AgnosticFileStorageError('No connection')


