#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import pytest
from six.moves import StringIO

import afs
import afs.afs_sftp


def test_create_afs_sftp():
    fs = afs.afs_sftp.SFTPFileStorage(
        'sftptest',
        host='srv-archivos',
        port=22,
        username='euribates',
        password='%SFTP_PASSWORD%',
    )
    assert fs.name == 'sftptest'
    assert fs.host == 'srv-archivos'
    assert fs.port == 22
    assert fs.address == ('srv-archivos', 22)
    assert fs.username == 'euribates'
    assert fs.client is None
    assert fs.transport is None
    assert fs.is_connected is False


# @pytest.fixture
# def mem_fs():
    # _fs = afs.afs_memory.MemoryFileStorage('memtest')
    # return _fs


# def test_memory_create_file(mem_fs):
    # with mem_fs as _fs:
        # buff = StringIO('Hola, mundo')
        # size = _fs.save('hola.txt', buff)
        # assert size == 11
        # assert _fs.is_file('hola.txt')
        # assert _fs.ls() == ['hola.txt']


# def test_memory_ls(mem_fs):
    # with mem_fs as _fs:
        # assert _fs.ls() == []
        # _fs.save('a.txt', StringIO('a'*32))
        # _fs.save('b.txt', StringIO('b'*32))
        # _fs.save('c.txt', StringIO('c'*32))
        # _fs.mkdir('tmp')
        # assert set(_fs.ls()) == set([
            # 'a.txt',
            # 'b.txt',
            # 'c.txt',
            # 'tmp',
            # ])


# def test_memory_current_dir(mem_fs):
    # with mem_fs as _fs:
        # assert _fs.current_dir == []


# def test_memory_mkdir(mem_fs):
    # with mem_fs as _fs:
        # _fs.mkdir('tmp')
        # files = _fs.ls()
        # assert files == ['tmp']
        # assert _fs.is_dir('tmp')


# def test_memory_rmdir(mem_fs):
    # with mem_fs as _fs:
        # _fs.mkdir('tmp')
        # assert _fs.is_dir('tmp')
        # _fs.rmdir('tmp')
        # assert not _fs.is_dir('tmp')


# def test_memory_cd(mem_fs):
    # with mem_fs as _fs:
        # _fs.mkdir('tmp')
        # assert _fs.ls() == ['tmp']
        # _fs.cd('tmp')
        # assert _fs.ls() == []


if __name__ == '__main__':
    pytest.main()
