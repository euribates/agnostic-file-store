#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import tempfile
from six.moves import StringIO

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
    with afs.connect('localtest') as fs:
        stream = StringIO(
            'hola, mundo reseña árbol épico '
            'ínclito único óbice'
        )
        size = fs.save('testigo.txt', stream)
        assert fs.is_file('testigo.txt')
        assert size == 56


@pytest.mark.skip
def test_save_image():
    afs.configure_dict({
        'localtemp': {
            'kind': 'local',
            'base': '/tmp',
            }
        })
    with afs.connect('localtmp') as fs:
        size = fs.save('escudo.png', open('./escudo.png', 'rb'))
        assert fs.is_file('escudo.png')
        assert size == 3514


@pytest.mark.skip
class TestRemoveFile(unittest.TestCase):

    def test_rm(self):
        test_filename = 'borrame.txt'
        with afs.connect('localtmp') as fs:
            self.assertFalse(fs.is_file(test_filename))
            fs.save(test_filename, StringIO('Dumb file'.encode('utf-8')))
            self.assertTrue(fs.is_file(test_filename))
            fs.rm(test_filename)
            self.assertFalse(fs.is_file(test_filename))

    def test_rm_nonexistent_file(self):
        '''Must return False and no error.
        '''
        with afs.connect('localtmp') as fs:
            self.assertFalse(fs.rm('nonexistent_file.txt'))

    def test_try_to_rm_a_dir_fails(self):
        '''Triying to remove a directory must fail.
        '''
        with afs.connect('localtmp') as fs:
            fs.mkdir('uno')
            with pytest.raises(Exception):
                fs.rm('uno')
            fs.rmdir('uno')


@pytest.mark.skip
class ChangeDir(unittest.TestCase):

    def setUp(self):
        os.mkdir('/tmp/uno')
        os.mkdir('/tmp/uno/dos')

    def test_cd(self):
        with afs.connect('localtmp') as fs:
            fs.cd('uno')
            self.assertEqual(fs.cwd(), ['uno'])
            self.assertEqual(fs.get_local_path(), '/tmp/uno')
            fs.cd('dos')
            self.assertEqual(fs.cwd(), ['uno', 'dos'])
            self.assertEqual(fs.get_local_path(), '/tmp/uno/dos')

    def tearDown(self):
        os.rmdir('/tmp/uno/dos')
        os.rmdir('/tmp/uno')


@pytest.mark.skip()
class TestUso(unittest.TestCase):

    def test_rmdir(self):
        test_dir = 'removable_dir'
        with afs.connect('localtmp') as fs:
            self.assertFalse(fs.is_dir(test_dir), 'Directory exists (It must NOT)')
            fs.mkdir(test_dir)
            self.assertTrue(fs.is_dir(test_dir), 'Directory doesn\'t exists (and it must)')
            fs.rmdir(test_dir)
            self.assertFalse(fs.is_dir(test_dir), 'Directory exists (It must NOT)')


if __name__ == '__main__':
    pytest.main()
