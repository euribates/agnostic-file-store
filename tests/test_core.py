#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import traceback
import unittest
import logging

from afs import env
from afs import core
from afs.exceptions import AgnosticFileStorageError


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def get_module_dir():
    return os.path.dirname(
        os.path.abspath(__file__)
        )


class TestAFSEntry(unittest.TestCase):

    def test___init__(self):
        entry = core.AFSEntry('readme.txt', 142)
        self.assertEqual(entry.name, 'readme.txt')
        self.assertEqual(entry.size, 142)


class TestAFSFile(unittest.TestCase):

    def test___str__(self):
        entry = core.AFSFile('readme.txt', 142)
        self.assertEqual(str(entry), 'readme.txt')

    def test_is_dir(self):
        entry = core.AFSFile('readme.txt', 142)
        self.assertFalse(entry.is_dir())

    def test_is_file(self):
        entry = core.AFSFile('readme.txt', 142)
        self.assertTrue(entry.is_file())


class TestAFSDirectory(unittest.TestCase):

    def test___str__(self):
        entry = core.AFSDirectory('etc', 10)
        self.assertEqual(str(entry), 'etc/')

    def test_is_dir(self):
        entry = core.AFSDirectory('etc', 10)
        self.assertTrue(entry.is_dir())

    def test_is_file(self):
        entry = core.AFSDirectory('etc', 10)
        self.assertFalse(entry.is_file())




class CWD(unittest.TestCase):

    def setUp(self):
        self.afs = core.AgnosticFileStorage('test_cwd')

    def test_cwd_root(self):
        self.assertEqual(self.afs.cwd(), [])
        
    def test_one_dir(self):
        self.afs.is_dir = lambda self: True
        self.afs.cd('one')
        self.assertEqual(self.afs.cwd(), ['one'])

    def test_two_dirs(self):
        self.afs.is_dir = lambda self: True
        self.afs.cd('one')
        self.afs.cd('two')
        self.assertEqual(self.afs.cwd(), ['one','two'])

class CD(unittest.TestCase):

    def setUp(self):
        self.afs = core.AgnosticFileStorage('test_cd')

    def test_cd_dir_ok(self):
        self.afs.is_dir = lambda self: True
        self.afs.cd('one')
        self.assertEqual(self.afs.cwd(), ['one'])

    def test_cd_dir_nonexistent(self):
        self.afs.is_dir = lambda self: False
        self.assertRaises(
            AgnosticFileStorageError,
            self.afs.cd,
            'nonexistent',
            )

class Config(unittest.TestCase):

    def test_get_options_filename(self):
        from afs import __file__ as afs_module_dir
        from afs import get_options_filename
        options = get_options_filename()
        self.assertEqual(options.next(), '/etc/afs.ini')
        user_config = os.path.join(
            os.path.expanduser('~'),
            'afs.ini'
            )
        self.assertEqual(options.next(), user_config)
        module_config = os.path.join(
            os.path.dirname(os.path.abspath(afs_module_dir)),
            'afs.ini',
            )
        self.assertEqual(options.next(), module_config)
        self.assertRaises(StopIteration, options.next)

    def test_call_connect_with_options_filename(self):
        from afs import connect
        local_config_file = os.path.join(
            get_module_dir(), 
            'afs-test-config.ini',
            )
        with connect('localtest', local_config_file) as fs:
            self.assertEqual(fs.base, '/tmp')

        with connect('smbtest', local_config_file) as fs:
            self.assertEqual(fs.username, 'jileon')
            self.assertEqual(fs.host, 'nas1')
            self.assertEqual(fs.domain, 'parcan.es')
            self.assertEqual(fs.service, 'test$')

if __name__ == '__main__':
    unittest.main()
