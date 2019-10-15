#!/usr/bin/env python3
"""examples on variable scope"""
__author__ = 'Yuchen YANG (YY5819@ic.ac.uk)'
__version__ = '0.0.1'
## Try this first

_a_global = 10

def a_function():
    _a_global = 5
    _a_local = 4
    print("Inside the function, the value is ", _a_global)
    print("Inside the function, the value is ", _a_local)
    return None

a_function()

print("Outside the function, the value is ", _a_global)


## Now try this

_a_global = 10

def a_function():
    global _a_global
    _a_global = 5
    _a_local = 4
    print("Inside the function, the value is ", _a_global)
    print("Inside the function, the value is ", _a_local)
    return None

a_function()
print("Outside the function, the value is", _a_global)

# first chunck of newer version shown at class

_a_global = 10

if _a_global >= 5:
    _b_global = _a_global + 5

def a_function():
    _a_global = 5
    
    if _a_global >= 5:
        _b_global =  _a_global + 5

    _a_local = 4

    print("inside the function, the value of _a_global is ", _a_global)
    print("inside the function, the value of _b_global is ", _b_global)
    print("inside the function, the value of _a_local is ", _a_local)

    return None

a_function()

print("outside the function, the value of _a_global is ", _a_global)    
print("outside the function, the value of _b_global is ", _b_global)    


# second chunck of newer version shown at class
_a_global = 10

def a_function():
    _a_local = 4

    print("inside the function, the value of _a_local is ", _a_local)
    print("inside the function, the value of _a_global is ", _a_global)

    return None

a_function()

print("outside the function, the value of _a_global is ", _a_global)


# third chunck of newer version shown at class
_a_global = 10

print("outside the function, the value of _a_global is ", _a_global)

def a_function():
    global _a_global
    _a_global = 5
    _a_local = 4

    print("inside the function, the value of _a_global is ", _a_global)
    print("inside the function, the value of _a_local is ", _a_local)

    return None

a_function()

print("outside the function, the value of _a_global now is ", _a_global)

# fourth chunck of newer version shown at class
def a_function():
    _a_global = 10

    def _a_function2():
        global _a_global
        _a_global = 20
    
    print("Before calling a_function, value of _a_global is ", _a_global)

    _a_function2()
    
    print("After calling _a_function2, value of _a_global is ", _a_global)

a_function()

print("The value of a_global in main workspace / namespace is ", _a_global)
