#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import


from .core import AgnosticFileStorage


class SFTPFileStorage(AgnosticFileStorage):

    def __init__(self, name, **kwargs):
        super(SFTPFileStorage, self).__init__(name)
        self.host = kwargs.get('host', 'localhost')
        self.port = int(kwargs.get('port', 22))
        self.address = (self.host, self.port)
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.transport = None
        self.client = None

    def open(self):
        import paramiko
        self.transport = paramiko.Transport(self.address)
        self.transport.connect(None, self.username, self.password)
        self.client = paramiko.SFTPClient.from_transport(self.transport)
        super(SFTPFileStorage, self).open()
        return self

    def close(self):
        if self.client:
            self.client.close()
        if self.transport:
            self.transport.close()
        self.transport = None
        self.client = None
        super(SFTPFileStorage, self).close()

    def _it_exists(self, filename):
        try:
            self.client.stat(filename)
            return True
        except IOError:
            return False

    def is_dir(self, name):
        if self._it_exists(name):
            try:
                self.client.chdir(name)
                self.client.chdir("..")
                return True
            except (IOError, paramiko.sftp.SFTPError):
                return False
        return False

    def is_file(self, name):
        raise Exception('Not implemented')
        # directory = self._find_current_directory()
        # assert isinstance(directory, dict)
        # entry = directory[name]
        # return not isinstance(entry, dict)

    def ls(self):
        return self.client.listdir('.')

    def mkdir(self, dir_name):
        raise Exception('Not implemented')
        # directory = self._find_current_directory()
        # directory[dir_name] = {}

    def rmdir(self, dir_name):
        raise Exception('Not implemented')

    def save(self, file_name, stream):
        raise Exception('Not implemented')
        # directory = self._find_current_directory()
        # data = stream.read()
        # directory[file_name] = data
        # return len(data)

    def rm(self, file_name):
        raise Exception('Not implemented')
