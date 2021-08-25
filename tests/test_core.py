#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import logging

import pytest

from afs import core


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


def get_module_dir():
    return os.path.dirname(
        os.path.abspath(__file__)
        )


def test_afs_entry_class_creation():
    entry = core.AFSEntry('readme.txt', 142)
    assert entry.name == 'readme.txt'
    assert entry.size == 142


@pytest.fixture
def with_file():
    return core.AFSFile('readme.txt', 142)


def test_asf_file_as_str(with_file):
    assert str(with_file) == 'readme.txt'


def test_asf_filed_is_dir_method_must_return_false(with_file):
    assert not with_file.is_dir()


def test_isf_file_is_file_must_return_true(with_file):
    assert with_file.is_file()


def test_asf_dir_as_str():
    entry = core.AFSDirectory('etc', 10)
    assert str(entry) == 'etc/'


def test_is_dir():
    entry = core.AFSDirectory('etc', 10)
    assert entry.is_dir()


def test_is_file():
    entry = core.AFSDirectory('etc', 10)
    assert not entry.is_file()


@pytest.fixture
def with_dir():
    afs = core.AgnosticFileStorage('test_cwd')
    afs.is_dir = lambda _: True
    return afs


def test_cwd_root(with_dir):
    assert with_dir.cwd() == []


def test_one_dir(with_dir):
    with_dir.cd('one')
    assert with_dir.cwd() == ['one']


def test_two_dirs(with_dir):
    with_dir.cd('one')
    with_dir.cd('two')
    assert with_dir.cwd() == ['one', 'two']


def test_cd_dir_ok(with_dir):
    with_dir.cd('one')
    assert with_dir.cwd() == ['one']


def test_cd_dir_non_exists():
    afs = core.AgnosticFileStorage('test')
    afs.is_dir = lambda _: False
    with pytest.raises(ValueError):
        afs.cd('nonexistent')


if __name__ == '__main__':
    pytest.main()
