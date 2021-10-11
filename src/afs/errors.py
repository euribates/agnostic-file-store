#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import


def no_connection():
    raise ValueError(
        "The AFS system is not connected."
        "You can't call any method until the conexion"
        "is open."
        )


def configuration_not_found():
    return ValueError(
        "Configuration file not found.\n"
        "Unable to find a suitable afs config file.\n"
        "Try to modify the afs-sample.ini to your own"
        " environment.\n"
        "I'll need and afs.ini file in one"
        " of this directories (All found files would be used):\n"
        " - /etc/afs.ini\n"
        " - afs.ini on your home directory\n"
        " - afs.ini on the afs installed directory\n"
        "Please note that values in last files"
        " supersedes the previous ones.\n"
        "Also, you can set the configuration file to be used"
        " as a second parameter in the connect call"
        " or use the special keyword `:memory:` to use a memory AFS."
        )


def can_not_delete_directory(name):
    return ValueError(
        "Can not delete {name} with method rm()"
        " because is a directory."
        " Use the rmdir() method.".format(name=name)
        )


def can_not_delete_file(name):
    return ValueError(
        "Can not delete {name} with method rmdir()"
        " because is a regular file."
        " Use the rm() method.".format(name=name)
        )


def config_file_not_found(kind, config_file):
    return ValueError(
        "Don't know how to handle this kind "
        "of file storage service: {k}.\n"
        "Configuration file is {f}."
        .format(k=kind, f=config_file)
        )


def directory_is_not_empty(dir_name):
    raise ValueError(
        "Can't delete directory {dir_name},"
        "it's not empty.".format(dir_name=dir_name)
    )


def read_error(dir_name, num_tries=0):
    return ValueError(
        "Can't read the content of {!r}"
        " (tried {} times)".format(
            dir_name,
            num_tries,
            )
    )
