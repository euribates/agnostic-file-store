#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import pytest

import afs


def test_afs_get_options_filename():
    options = afs.get_options_filename()
    for path in options:
        assert path.endswith('afs.ini')


@pytest.mark.skip
def test_call_connect_with_options_filename():
    local_config_file = 'afs-test-config.ini'
    with afs.connect('localtest', local_config_file) as _fs:
        assert _fs.base == '/tmp'

    with afs.connect('smbtest', local_config_file) as _fs:
        assert _fs.username == 'jileon'
        assert _fs.host == 'nas1'
        assert _fs.domain == 'parcan.es'
        assert _fs.service == 'test$'


if __name__ == '__main__':
    pytest.main()
