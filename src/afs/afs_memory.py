#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from . import errors
from .core import AgnosticFileStorage


class MemoryFileStorage(AgnosticFileStorage):

    def __init__(self, name, **kwargs):
        """Initialize with the suplied parameters.

        Do not forget to call super.__init__ to set the
        name.
        """
        super(MemoryFileStorage, self).__init__(name)
        self.root = {}

    def open(self):
        """Open connections and this kind of stuff goes here.
        """
        #  Your code here
        pass
        #  Don't forget to call super.close and return self
        super(MemoryFileStorage, self).open()
        return self

    def close(self):
        """Close connections and this kind of stuff goes here.
        """
        #  Your code here
        pass
        #  Don't forget to call super.close
        super(MemoryFileStorage, self).close()

    def _locate_current_directory(self):
        dict_dir = self.root
        for path in self.current_dir:
            dict_dir = dict_dir[path]
        return dict_dir

    def is_dir(self, name):
        directory = self._locate_current_directory()
        assert isinstance(directory, dict)
        if name in directory:
            entry = directory[name]
            return isinstance(entry, dict)
        return False

    def is_file(self, name):
        directory = self._locate_current_directory()
        assert isinstance(directory, dict)
        if name in directory:
            entry = directory[name]
            return not isinstance(entry, dict)
        return False

    def ls(self):
        directory = self._locate_current_directory()
        return list(directory)

    def mkdir(self, name):
        directory = self._locate_current_directory()
        directory[name] = {}

    def rmdir(self, name):
        directory = self._locate_current_directory()
        if name not in directory:
            return
        content = directory[name]
        if not isinstance(content, dict):
            raise errors.can_not_delete_file(name)
        if content:
            raise errors.directory_is_not_empty(name)
        del directory[name]

    def save(self, file_name, stream):
        directory = self._locate_current_directory()
        data = stream.read()
        directory[file_name] = data
        return len(data)

    def rm(self, name):
        directory = self._locate_current_directory()
        if name not in directory:
            return
        content = directory[name]
        if isinstance(content, dict):
            raise errors.can_not_delete_directory(name)
        del directory[name]



        directory = self._locate_current_directory()
        content = directory.get(dir_name, {})

        if filename:
            raise errors.directory_is_not_empty(dir_name)
        if dir_name in directory:
            del directory[dir_name]
