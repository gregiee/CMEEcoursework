#!/usr/bin/env python3
"""run Lotka-Volterra Model profile"""

__author__ = 'Yuchen YANG (YY5819@ic.ac.uk)'
__version__ = '0.0.1'

import os
# # cprofile in python allows more methods to deal with profile
# import cProfile

os.system("python -m cProfile LV1.py")
os.system("python -m cProfile LV2.py 1 0.1 1.5 0.75 4300")
os.system("python -m cProfile LV3.py 1 0.1 1.5 0.75 38")
os.system("python -m cProfile LV3.py 1 0.1 1.5 0.75 18")