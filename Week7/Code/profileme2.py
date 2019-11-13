#!/usr/bin/env python3
"""profile example"""

__author__ = 'Yuchen YANG (YY5819@ic.ac.uk)'
__version__ = '0.0.1'


def my_squares(iters):
    """a list comprehension to create a list of square numbers til input iters"""
    out = [i ** 2 for i in range(iters)]
    return out

def my_join(iters, string):
    """ create comma seperated string based on given string for iter time """
    out = ''
    for i in range(iters):
        out += ", " + string
    return out

def run_my_funcs(x,y):
    """ run my_squre and my_join using x and y """
    print(x,y)
    my_squares(x)
    my_join(x,y)
    return 0

run_my_funcs(10000000,"My string")