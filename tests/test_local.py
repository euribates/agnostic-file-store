#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

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
def tmp_file():
    file_name = '/tmp/afs_token.txt'
    with open(file_name, 'w') as f:
        f.write('1234\n')
    yield f
    os.unlink(file_name)


@pytest.mark.skip
def test_ls(tmp_file):
    with afs.connect('localtmp') as fs:
        found = False
        for item in fs.ls():
            if item.name == 'token.txt':
                assert item.size == 5
                found = True
            assert_archive_or_dir(item)
        assert found, 'File token.txt not found'


@pytest.mark.skip
def test_afs_connect():
    with afs.connect('localtmp') as fs:
        assert fs.name == 'localtmp'
        assert fs.base == '/tmp'
        assert fs.is_connected
        assert fs.get_local_path('hola.txt') == '/tmp/hola.txt'


@pytest.mark.skip
class TestMakeDir(unittest.TestCase):

    def setUp(self):
        self.assertFalse(os.path.isdir('/tmp/test_dir'))

    def tearDown(self):
        self.assertTrue(os.path.isdir('/tmp/test_dir'))
        os.rmdir('/tmp/test_dir')

    def test_mkdir(self):
        with afs.connect('localtmp') as fs:
            self.assertFalse(fs.is_dir('test_dir'))
            fs.mkdir('test_dir')
            self.assertTrue(fs.is_dir('test_dir'))


@pytest.mark.skip
class TestSaveFiles(unittest.TestCase):

    def test_save_text(self):
        with afs.connect('localtmp') as fs:
            stream = StringIO(
                'hola, mundo reseña árbol épico '
                'ínclito único óbice'.encode('utf-8')
                )
            size = fs.save('testigo.txt', stream)
            self.assertTrue(fs.is_file('testigo.txt'))
            self.assertEqual(size, 56)


    def test_save_image(self):
        with afs.connect('localtmp') as fs:
            size = fs.save('escudo.png', open('/home/jileon/wwwroot/art/escudo.png', 'rb'))
            self.assertTrue(fs.is_file('escudo.png'))
            self.assertEqual(size, 3514)

    def test_save_image_from_pil(self):
        from PIL import Image, ImageDraw
        size = (256, 256)
        im = Image.new("RGB", size, "white")
        draw = ImageDraw.Draw(im)
        draw.line((0, 0) + im.size, fill=128)
        draw.line((0, im.size[1], im.size[0], 0), fill=128)
        with afs.connect('localtmp') as fs:
            buff = StringIO()
            im.save(buff, format="PNG")
            buff.seek(0)
            fs.save('imagen.png', buff)


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
