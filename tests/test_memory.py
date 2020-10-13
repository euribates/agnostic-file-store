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
import afs.afs_memory
from afs.exceptions import AgnosticFileStorageError

class Create(unittest.TestCase):

    def test(self): 
        fs = afs.afs_memory.MemoryFileStorage('memtest')
        self.assertFalse(fs.is_connected)
        with fs:
            self.assertTrue(fs.is_connected)
        self.assertFalse(fs.is_connected)


if __name__ == '__main__':
    unittest.main()
