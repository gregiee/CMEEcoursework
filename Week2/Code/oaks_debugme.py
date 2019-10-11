#!/usr/bin/env python3

"""Some functions exemplifying the use of control statements"""

__author__ = 'Your Name (Your.Name@your.email.address)'
__version__ = '0.0.1'

import csv
import sys
import ipdb
import doctest
import re

def is_an_oak(name):

    """
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
    #Define function to be tested
    #print("i'm here in the oak function!")
    #print(name.lower().startswith('quercs'))
    #ipdb.set_trace()
    #the function works with "genus", found the typo in 'quercs'
    # return name.lower().startswith('quercus')
    if re.match(r"^quer?cuss?$", name, flags=re.I) != None:
        return True
    else:
        return False

def main(argv): 
    f = open('../Data/TestOaksData.csv','r')
    g = open('../Data/JustOaksData.csv','w')
    next(f)
    taxa = csv.reader(f)
    fieldnames = ['Genus', 'Species']
    csvwrite = csv.DictWriter(g,fieldnames=fieldnames)
    oaks = set()
    csvwrite.writeheader()
    for row in taxa:
        print(row)
        print ("The genus is: ") 
        print(row[0] + '\n')
        if is_an_oak(row[0]):
            print('FOUND AN OAK!\n')
            csvwrite.writerow({'Genus': row[0], 'Species': row[1]})    
    return 0


if (__name__ == "__main__"):
    status = main(sys.argv)

doctest.testmod()