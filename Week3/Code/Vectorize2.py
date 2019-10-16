#!/usr/bin/env python3

""" two ways of running stochastic Ricker and show speed differences"""

__author__ = 'Yuchen Yang (yy5819@ic.ac.uk)'
__version__ = '0.0.1'

import numpy as np
import time

# create function using nested loops
def stochrick(p0=np.random.uniform(size=1000,low=.5,high=1.5),r=1.2,K=1,sigma=0.2,numyears=100):
    N=np.zeros((numyears, len(p0)))
    N[1,:]=p0
    for pop in range(0, len(p0)):
        for yr in range(1, numyears):
            N[yr,pop]=N[yr-1,pop]*np.exp(r*(1-N[yr-1,pop]/K)+np.random.normal(0,sigma,1))
    return N

def stochrickvect(p0=np.random.uniform(size=1000,low=.5,high=1.5),r=1.2,K=1,sigma=0.2,numyears=100):
    N=np.zeros((numyears, len(p0)))
    N[1,:]=p0
    for yr in range(1, numyears):
        N[yr,]=N[yr-1,]*np.exp(r*(1-N[yr-1,]/K)+np.random.normal(0,sigma,1))
    return N

# bash output
tic_nested_loop=time.time()
stochrick()
toc_nested_loop=time.time()
print("time spent for loop:")
print(toc_nested_loop-tic_nested_loop)
print("================================")
tic_vect=time.time()
stochrickvect()
toc_vect=time.time()
print("time spent for vect:")
print(toc_vect-tic_vect)