#!/usr/bin/python3
"""
Utility functions
"""

from sys import stdin, stdout, stderr

INPUT = stdin
OUTPUT = stdout
LOG = stderr
HEDGES = tuple("the at of a on to by for as so from in are over".split())

def unique(iterable):
    "Iterate items only once"
    seen = set()
    for item in iterable:
        if item in seen:
            continue
        seen.add(item)
        yield item

def log(*msg, **kwargs):
    "Log to LOG, called like print()"
    print(":::", end="", file=LOG)
    print(*msg, **kwargs, file=LOG)
