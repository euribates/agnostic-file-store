#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os
from . import log
from .core import AgnosticFileStorage

logger = log.get_logger(__name__)

class MemoryFileStorage(AgnosticFileStorage):

    def __init__(self, name, **kwargs):
        super(MemoryFileStorage, self).__init__(name)
        self.is_connected = False
        self.root = {}
    
    @log.trace(logger)
    def open(self):
        self.is_connected = True

    @log.trace(logger)
    def close(self):
        self.is_connected = False




