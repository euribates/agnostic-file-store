#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from six.moves import StringIO

import os
import unittest

import env

import afs
from afs.exceptions import AgnosticFileStorageError


def assert_archive_or_dir(item):
    if isinstance(item, (afs.core.AFSFile, afs.core.AFSDirectory)):
        return
    raise AssertionError(
        'Expected a AFSFile or AFSDirectory item, but it gets '
        'an object of class {}'.format(
            item.__class__.__name__
            )
        )

class ListFiles(unittest.TestCase):

    def setUp(self):
        with open('/tmp/token.txt', 'wb') as f:
            f.write('1234\n')

    def tearDown(self):
        os.unlink('/tmp/token.txt')

    def test_ls(self):
        with afs.connect('localtmp') as fs:
            found = False
            for item in fs.ls():
                if item.name == 'token.txt':
                    self.assertEqual(item.size, 5)
                    found = True
                assert_archive_or_dir(item)
            self.assertTrue(found, 'File token.txt not found')
            

class Connect(unittest.TestCase):

    def test_connect(self):
        with afs.connect('localtmp') as fs:
            self.assertEqual(fs.name, 'localtmp')
            self.assertEqual(fs.base, '/tmp')
            self.assertTrue(fs.is_connected)
            self.assertEqual(
                fs.get_local_path('hola.txt'),
                '/tmp/hola.txt',
                )

class MakeDir(unittest.TestCase):

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


class SaveFiles(unittest.TestCase):

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


class RemoveFile(unittest.TestCase):

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
            self.assertRaises(AgnosticFileStorageError, fs.rm, 'uno',)
            fs.rmdir('uno')

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

class Uso(unittest.TestCase):

    def test_rmdir(self):
        test_dir = 'removable_dir'
        with afs.connect('localtmp') as fs:
            self.assertFalse(fs.is_dir(test_dir), 'Directory exists (It must NOT)')
            fs.mkdir(test_dir)
            self.assertTrue(fs.is_dir(test_dir), 'Directory doesn\'t exists (and it must)')
            fs.rmdir(test_dir)
            self.assertFalse(fs.is_dir(test_dir), 'Directory exists (It must NOT)')


if __name__ == '__main__':
    unittest.main()