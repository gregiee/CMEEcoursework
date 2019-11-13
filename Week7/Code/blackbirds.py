#!/usr/bin/env python3
"""regex practical"""

__author__ = 'Yuchen YANG (YY5819@ic.ac.uk)'
__version__ = '0.0.1'

import re
import ipdb

# Read the file (using a different, more python 3 way, just for fun!)
with open('../Data/blackbirds.txt', 'r') as f:
    text = f.read()

# replace \t's and \n's with a spaces:
text = text.replace('\t',' ')
text = text.replace('\n',' ')
# You may want to make other changes to the text. 

# In particular, note that there are "strange characters" (these are accents and
# non-ascii symbols) because we don't care for them, first transform to ASCII:

text = text.encode('ascii', 'ignore') # first encode into ascii bytes
text = text.decode('ascii', 'ignore') # Now decode back to string

# Now extend this script so that it captures the Kingdom, Phylum and Species
# name for each species and prints it out to screen neatly.

# print(text)
my_reg = r'(Kingdom)\s+([a-zA-Z]+)\s+.+?(Phylum)\s+([a-zA-Z]+)\s+.+?(Species)\s+([a-zA-Z]+\s[a-zA-Z]+)' 
Species = re.findall(my_reg, text)

# ipdb.set_trace()

for i in Species:
	print(i[0] + ":" + i[1])
	print(i[2] + ":" + i[3])
	print(i[4] + ":" + i[5])
	print("===============")
# Hint: you may want to use re.findall(my_reg, text)... Keep in mind that there
# are multiple ways to skin this cat! Your solution could involve multiple
# regular expression calls (easier!), or a single one (harder!)