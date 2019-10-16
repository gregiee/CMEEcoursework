#!/usr/bin/env python3

""" two ways of running stochastic Ricker and show speed differences"""

__author__ = 'Yuchen Yang (yy5819@ic.ac.uk)'
__version__ = '0.0.1'

import numpy as np
import time

# create 1000*1000 random number
M = np.random.rand(1000,1000)

def SumAllElements_loop(M):
    """using loop to sum all numbers up"""
    Tot = 0
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            Tot += M[i][j]
    return Tot

def SumAllElements_vec(M):
    """vec method"""
    Tot = np.sum(M)
    return Tot
 
# bash output
tic_nested_loop=time.time()
SumAllElements_loop(M)
toc_nested_loop=time.time()
print("time spent for loop:")
print(toc_nested_loop-tic_nested_loop)
print("================================")

tic_vect=time.time()
SumAllElements_vec(M)
toc_vect=time.time()
print("time spent for vect:")
print(toc_vect-tic_vect)
