#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import socket

import smb
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
        if self.username:
            self.username = self.username.encode('utf-8')
        else:
            raise ValueError('Unknown SMB user for {}'.format(name))
        self.password = self.get_value(kwargs, 'password')
        if self.password:
            self.password = self.password.encode('utf-8')
        else:
            raise ValueError('Unknown SMB password for {}'.format(name))
        self.host = self.get_value(kwargs, 'host').encode('utf-8')
        self.client = socket.gethostname()
        self.domain = self.get_value(kwargs, 'domain').encode('utf-8')
        self.service = self.get_value(kwargs, 'service').encode('utf-8')
        self.fqn = '{}.{}'.format(self.host, self.domain)
        self.server_ip = socket.gethostbyname(self.fqn)
        self.is_connected = False

    def __str__(self):
        bar = '-' * (59 - len(self.name))
        buff = ['--[ SMBFileStorage {} ]{}'.format(self.name, bar)]
        buff.append('username: {}'.format(self.username))
        buff.append('host: {}'.format(self.host))
        buff.append('client {}'.format(self.client))
        buff.append('domain: {}'.format(self.domain))
        buff.append('service: {}'.format(self.service))
        buff.append('fqn: {}'.format(self.fqn))
        buff.append('server IP: {}'.format(self.server_ip))
        buff.append('Current dir: {}'.format(self.current_dir))
        buff.append('Is Connected: {}'.format(self.is_connected))
        buff.append('-'*80)
        return '\n'.join(buff)

    def open(self):
        self.conn = smb.SMBConnection(
            self.username,
            self.password,
            self.client,
            self.host,
            self.domain,
            use_ntlm_v2=False,
            sign_options=smb.SMBConnection.SIGN_NEVER,
            is_direct_tcp=True,
            )
        self.is_connected = self.conn.connect(self.server_ip, 445)
        return self

    def close(self):
        self.conn.close()
        self.is_connected = False

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


