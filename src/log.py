#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import logging

from logging import CRITICAL, ERROR, DEBUG, WARNING, INFO

DEFAULT_LOG_LEVEL = WARNING

def get_logger(name, level=DEFAULT_LOG_LEVEL):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

def trace(logger):
    def trace_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            buff = ['Called {}('.format(func.__name__)]
            if args:
                buff.append(', '.join([repr(_) for _ in args]))
            if kwargs:
                buff.append(', '.join([
                    '{}={}'.format(_, kwargs[_]) for _ in kwargs
                    ]))
            buff.append(')')
            logger.info(''.join(buff))
            result = func(*args, **kwargs)
            logger.info('{} returned {}'.format(func.__name__, result))
            return result
        return wrapper
    return trace_decorator

