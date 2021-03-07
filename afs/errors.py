#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import


def no_conexion():
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


def rm_can_not_delete_directories():
    return ValueError(
        "Can't delete a directory with method rm().\n"
        "Use the rmdir() method."
        )
