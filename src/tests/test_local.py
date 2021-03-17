#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import tempfile
from six import StringIO, BytesIO

import os
import unittest

import pytest

import afs


def assert_archive_or_dir(item):
    if isinstance(item, (afs.core.AFSFile, afs.core.AFSDirectory)):
        return
    raise AssertionError(
        'Expected a AFSFile or AFSDirectory item, but it gets '
        'an object of class {}'.format(
            item.__class__.__name__
            )
        )


@pytest.fixture
def create_tmp_filesystem():
    temp_dir = tempfile.TemporaryDirectory(dir='/tmp')
    file_name = 'afs_token.txt'
    full_name = os.path.join(temp_dir.name, file_name)
    with open(full_name, 'w') as f:
        f.write('1234\n')
    afs.add_source('localtest', {
        "kind": "local",
        "base": temp_dir.name,
        })
    yield temp_dir.name
    os.unlink(full_name)


def test_ls(create_tmp_filesystem):
    with afs.connect('localtest') as fs:
        found = False
        for item in fs.ls():
            if item.name == 'afs_token.txt':
                assert item.size == 5
                found = True
            assert_archive_or_dir(item)
        assert found, 'File token.txt not found'


def test_afs_connect(create_tmp_filesystem):
    with afs.connect('localtest') as fs:
        assert fs.name == 'localtest'
        assert fs.base == create_tmp_filesystem
        assert fs.is_connected


def test_afs_get_local_path(create_tmp_filesystem):
    with afs.connect('localtest') as fs:
        expected = os.path.join(create_tmp_filesystem, 'hola.txt')
        assert fs.get_local_path('hola.txt') == expected


def test_make_a_dir(create_tmp_filesystem):
    with afs.connect('localtest') as fs:
        assert fs.is_dir('test_dir') is False
        fs.mkdir('test_dir')
        assert fs.is_dir('test_dir')


def test_save_text(create_tmp_filesystem):
    source = (
            'hola, mundo reseña árbol épico '
            'ínclito único óbice'
        )
    with afs.connect('localtest') as fs:
        stream = StringIO(source)
        size = fs.save('testigo.txt', stream)
        assert fs.is_file('testigo.txt')
        assert size == 50
        filename = os.path.join(create_tmp_filesystem, 'testigo.txt')
        with open(filename, 'r') as f:
            assert f.read() == source


def test_save_binary(create_tmp_filesystem):
    source = (
        b'\x00\x01\x02\x03\x04\x05\x06\x07'
        b'\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
        b'\x10\x11\x12\x13\x14\x15\x16\x17'
        b'\x18\x19\x1A\x1B\x1C\x1D\x1E\x1F'
    )
    with afs.connect('localtest') as fs:
        stream = BytesIO(source)
        size = fs.save('output.bin', stream)
        assert size == 32
        filename = os.path.join(create_tmp_filesystem, 'output.bin')
        with open(filename, 'rb') as f:
            assert f.read() == source


def test_remove_file(create_tmp_filesystem):
    test_filename = 'borrame.txt'
    with afs.connect('localtest') as fs:
        assert not fs.is_file(test_filename)
        fs.save(test_filename, StringIO('Dumb file'))
        assert fs.is_file(test_filename)
        was_deleted = fs.rm(test_filename)
        assert was_deleted
        assert not fs.is_file(test_filename)


def test_remove_non_existent_file(create_tmp_filesystem):
    '''Must return False and no error.
    '''
    with afs.connect('localtest') as fs:
        assert fs.rm('nonexistent_file.txt') is False


def test_try_to_rm_a_dir_fails(create_tmp_filesystem):
    '''Triying to remove a directory must fail.
    '''
    with afs.connect('localtest') as fs:
        fs.mkdir('uno')
        with pytest.raises(ValueError):
            fs.rm('uno')
        fs.rmdir('uno')


def test_cd(create_tmp_filesystem):
    base = create_tmp_filesystem
    os.makedirs(os.path.join(base, 'uno/dos'))
    with afs.connect('localtest') as fs:
        fs.cd('uno')
        assert fs.cwd() == ['uno']
        assert fs.get_local_path() == os.path.join(base, 'uno')
        fs.cd('dos')
        assert fs.cwd(), ['uno' == 'dos']
        assert fs.get_local_path() == os.path.join(base, 'uno', 'dos')


def test_rmdir(create_tmp_filesystem):
    with afs.connect('localtest') as fs:
        assert not fs.is_dir('etc')
        fs.mkdir('etc')
        assert fs.is_dir('etc')
        fs.rmdir('etc')
        assert not fs.is_dir('etc')


if __name__ == '__main__':
    pytest.main()
