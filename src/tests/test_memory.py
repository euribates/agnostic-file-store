#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import pytest
from six import StringIO, BytesIO

import afs
import afs.afs_memory


def test_create_afs_in_memory():
    fs = afs.afs_memory.MemoryFileStorage('memtest')
    assert not fs.is_connected
    with fs:
        assert fs.is_connected
    assert not fs.is_connected


@pytest.fixture
def mem_fs():
    _fs = afs.afs_memory.MemoryFileStorage('memtest')
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
        assert _fs.ls() == []
        _fs.save('a.txt', StringIO('a'*32))
        _fs.save('b.txt', StringIO('b'*32))
        _fs.save('c.txt', StringIO('c'*32))
        _fs.mkdir('tmp')
        assert set(_fs.ls()) == set([
            'a.txt',
            'b.txt',
            'c.txt',
            'tmp',
            ])


def test_memory_current_dir(mem_fs):
    with mem_fs as _fs:
        assert _fs.current_dir == []


def test_memory_mkdir(mem_fs):
    with mem_fs as _fs:
        _fs.mkdir('tmp')
        files = _fs.ls()
        assert files == ['tmp']
        assert _fs.is_dir('tmp')


def test_memory_rmdir(mem_fs):
    with mem_fs as _fs:
        _fs.mkdir('tmp')
        assert _fs.is_dir('tmp')
        _fs.rmdir('tmp')
        assert not _fs.is_dir('tmp')


def test_memory_cd(mem_fs):
    with mem_fs as _fs:
        _fs.mkdir('tmp')
        assert _fs.ls() == ['tmp']
        _fs.cd('tmp')
        assert _fs.ls() == []


def test_save_text(mem_fs):
    source = (
            'hola, mundo reseña árbol épico '
            'ínclito único óbice'
        )
    with mem_fs as _fs:
        stream = StringIO(source)
        size = _fs.save('testigo.txt', stream)
        assert size == 50
        assert _fs.is_file('testigo.txt')


def test_save_binary(mem_fs):
    source = (
        b'\x00\x01\x02\x03\x04\x05\x06\x07'
        b'\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
        b'\x10\x11\x12\x13\x14\x15\x16\x17'
        b'\x18\x19\x1A\x1B\x1C\x1D\x1E\x1F'
    )
    with mem_fs as _fs:
        stream = BytesIO(source)
        size = _fs.save('output.bin', stream)
        assert size == 32
        assert _fs.is_file('output.bin')


if __name__ == '__main__':
    pytest.main()
