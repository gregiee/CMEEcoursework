#!/usr/bin/env python3

__author__ = 'Yuchen YANG (YY5819@ic.ac.uk)'
__version__ = '0.0.1'

import sys


# What does each of foo_x do? 
# calculating the square root of x
def foo_1(x): 
    # print here to keep the fucntion returns a float
    print('suqare root to' + str(x) + 'is: ')
    return x ** 0.5

# compare two numbers and spitting out the bigger one
def foo_2(x, y):
    print('the greater one is: ')
    if x > y:
        return x
    return y

# order three numbers in ascending order
def foo_3(x, y, z):
    if x > y:
        # tmp is a place holder in order to switch values between x and y
        tmp = y
        y = x
        x = tmp
    if y > z:
        tmp = z
        z = y
        y = tmp
    print('given numbers in ascending order: ')
    return [x, y, z]

# calculate the factorial of x, specifying (1, x+1) in range since range by default starts with 0.
def foo_4(x):
    result = 1
    for i in range(1, x + 1):
        result = result * i
    print(str(x) + '! is: ')
    return result

# a recursive function that calculates the factorial of x
def foo_5(x): 
    print(str(x) + '! is: ')
    if x == 1:
        return 1
    return x * foo5(x - 1)

# Calculate the factorial of x in a different way
def foo_6(x): 
    print(str(x) + '! is: ')
    facto = 1
    while x >= 1:
        facto = facto * x
        x = x - 1
    return facto

def main(argv):
    print(foo_1(69))
    print(foo_2(10,11))
    print(foo_3(2,1,23))
    print(foo_4(10))
    print(foo_5(10))
    print(foo_6(10))
    return 0

if (__name__ == "__main__"):
    status = main(sys.argv)
    sys.exit(status)