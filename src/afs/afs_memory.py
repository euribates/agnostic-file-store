#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from .core import AgnosticFileStorage


class MemoryFileStorage(AgnosticFileStorage):

    def __init__(self, name, **kwargs):
        super(MemoryFileStorage, self).__init__(name)
        self.root = {} 

    def _find_current_directory(self):
        dict_dir = self.root
        for path in self.current_dir:
            dict_dir = dict_dir[path]
        return dict_dir

    def is_dir(self, name):
        directory = self._find_current_directory()
        assert isinstance(directory, dict)
        entry = directory[name]
        return isinstance(entry, dict)

    def is_file(self, name):
        directory = self._find_current_directory()
        assert isinstance(directory, dict)
        entry = directory[name]
        return not isinstance(entry, dict)

    def ls(self):
        directory = self._find_current_directory()
        return list(directory)

    def mkdir(self, dir_name):
        directory = self._find_current_directory()
        directory[dir_name] = {}

    def save(self, file_name, stream):
        directory = self._find_current_directory()
        data = stream.read()
        directory[file_name] = data
        return len(data)
