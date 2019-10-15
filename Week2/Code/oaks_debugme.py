#!/usr/bin/env python3
"""
found and fixed the typo bug, added unit test to make sure the function
work as expected, add regex rules to take ambiguous inputs, add codes 
to deal with csv header for file read and write. 
"""
__author__ = 'Yuchen YANG (YY5819@ic.ac.uk)'
__version__ = '0.0.1'

import csv
import sys
# import ipdb
import doctest
import re

def is_an_oak(name):
    """ see if the input matches the rule i set
        
        >>> is_an_oak('Fagus sylvatica') 
        False

        >>> is_an_oak('quercus') 
        True

        >>> is_an_oak('Quercus') 
        True

        >>> is_an_oak('Quercuss') 
        True

        >>> is_an_oak('Quercusss') 
        False

        >>> is_an_oak('Quecuss') 
        True

    """

    # Define function to be tested
    # print("i'm here in the oak function!")
    # print(name.lower().startswith('quercs'))
    # ipdb.set_trace()
    # the function works with "genus", found the typo in 'quercs'
    # # return name.lower().startswith('quercs')
    # adding regex to take fuzz input
    # the regex rule takes an alternative extra s
    # and an alternative missing r as variations to quercus
    # and disregard capital letters 
    if re.match(r"^quer?cuss?$", name, flags=re.I) != None:
        return True
    else:
        return False

def main(argv): 
    """main control to determine if data entries in a file is oak and write to a new file."""
    f = open('../Data/TestOaksData.csv','r')
    g = open('../Data/JustOaksData.csv','w')
    next(f) #skip the header
    taxa = csv.reader(f)
    #set headers for new file
    fieldnames = ['Genus', 'Species'] 
    csvwrite = csv.DictWriter(g,fieldnames=fieldnames)
    csvwrite.writeheader()
    # commented out since not used
    # oaks = set()
    for row in taxa:
        print(row)
        print ("The genus is: ") 
        print(row[0] + '\n')
        if is_an_oak(row[0]):
            print('FOUND AN OAK!\n')
            csvwrite.writerow({'Genus': row[0], 'Species': row[1]})
    return 0


if __name__ == "__main__":
    status = main(sys.argv)

doctest.testmod()