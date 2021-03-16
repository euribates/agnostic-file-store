#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import pytest

import afs


def test_call_connect_local():
    afs.add_source('localtest', {
        'kind': 'local',
        'base': '/tmp',
    })
    with afs.connect('localtest') as _fs:
        assert _fs.base == '/tmp'


def test_call_connect_smb():
    afs.add_source('smbtest', {
        'kind': 'smb',
        'username': 'jileon',
        'host': 'localhost',
        'domain': '',
        'service': 'test$',
        'password': 'dfbef574829',
    })
    _fs = afs.sources['smbtest']
    assert _fs.username == b'jileon'
    assert _fs.host == b'localhost'
    assert _fs.domain == b''
    assert _fs.service == b'test$'


def test_call_connect_memory():
    afs.add_source('memtest', {
        'kind': 'memory',
    })
    with afs.connect('memtest') as _fs:
        assert _fs.root == {}


if __name__ == '__main__':
    pytest.main()
