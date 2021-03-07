#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import pytest
from six.moves import StringIO

import afs
import afs.afs_memory


def test_create_afs_in_memory():
    fs = afs.afs_memory.MemoryFileStorage(':memory:')
    assert not fs.is_connected
    with fs:
        assert fs.is_connected
    assert not fs.is_connected


@pytest.fixture
def mem_fs():
    _fs = afs.afs_memory.MemoryFileStorage(':memory:')
    assert isinstance(_fs, afs.afs_memory.MemoryFileStorage)
    return _fs


def test_memory_create_file(mem_fs):
    with mem_fs as _fs:
        buff = StringIO('Hola, mundo')
        size = _fs.save('hola.txt', buff)
        assert size == 11
        assert _fs.is_file('hola.txt')
        assert _fs.ls() == ['hola.txt']


def test_memory_ls(mem_fs):
    with mem_fs as _fs:
        files = _fs.ls()
        assert files == []


def test_memory_current_dir(mem_fs):
    with mem_fs as _fs:
        assert _fs.current_dir == []


def test_memory_mkdir(mem_fs):
    with mem_fs as _fs:
        _fs.mkdir('tmp')
        files = _fs.ls()
        assert files == ['tmp']
        assert _fs.is_dir('tmp')


def test_memory_cd(mem_fs):
    with mem_fs as _fs:
        _fs.mkdir('tmp')
        assert _fs.ls() == ['tmp']
        _fs.cd('tmp')
        assert _fs.ls() == []



if __name__ == '__main__':
    pytest.main()
