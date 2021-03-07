#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import


class AgnosticFileStorageError(ValueError):
    pass


class ConfigurationFileNotFound(ValueError):

    def __init__(self):
        msg = (
            "Configuration file not found\n\n"
            "Unable to find a suitable afs config file.\n"
            "Try to modify the afs-sample.ini to your own"
            " environment.\n"
            "I'll need and afs.ini file in one"
            " of this directories (All found files would be used):\n"
            " * /etc/afs.ini\n"
            " * afs.ini on your home directory\n"
            " * afs.ini on the afs installed directory\n"
            "Please note that values in last files"
            " supersedes the previous ones.\n"
            "Also, you can set the configuration file to be used"
            " as a second parameter in the connect call."
            )
        super(ConfigurationFileNotFound, self).__init__(msg)
        

def configuration_not_found():
    msg = (
        "Configuration file not found\n\n"
        "Unable to find a suitable afs config file.\n"
        "Try to modify the afs-sample.ini to your own"
        " environment.\n"
        "I'll need and afs.ini file in one"
        " of this directories (All found files would be used):\n"
        " * /etc/afs.ini\n"
        " * afs.ini on your home directory\n"
        " * afs.ini on the afs installed directory\n"
        "Please note that values in last files"
        " supersedes the previous ones.\n"
        "Also, you can set the configuration file to be used"
        " as a second parameter in the connect call"
        " or use the special keyword `:memory:` to usa a memory FS."
        )
    return ValueError(msg)


