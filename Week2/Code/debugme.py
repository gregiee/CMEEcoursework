#!/usr/bin/env python3
"""example script to debug"""

__author__ = 'Yuchen YANG (YY5819@ic.ac.uk)'
__version__ = '0.0.1'

def createabug(x):
    y = x**4
    z = 0.
    import pdb; pdb.set_trace()
    y = y/z
    return y

createabug(25)
