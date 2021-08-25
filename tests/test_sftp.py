#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import pytest

import afs


def test_create_afs_sftp():
    fs = afs.SFTPFileStorage(
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


if __name__ == '__main__':
    pytest.main()
