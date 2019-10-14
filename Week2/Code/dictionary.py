#!/usr/bin/env python3

__author__ = 'Yuchen YANG (YY5819@ic.ac.uk)'
__version__ = '0.0.1'

taxa = [ ('Myotis lucifugus','Chiroptera'),
         ('Gerbillus henleyi','Rodentia',),
         ('Peromyscus crinitus', 'Rodentia'),
         ('Mus domesticus', 'Rodentia'),
         ('Cleithrionomys rutilus', 'Rodentia'),
         ('Microgale dobsoni', 'Afrosoricida'),
         ('Microgale talazaci', 'Afrosoricida'),
         ('Lyacon pictus', 'Carnivora'),
         ('Arctocephalus gazella', 'Carnivora'),
         ('Canis lupus', 'Carnivora'),
        ]

# Write a short python script to populate a dictionary called taxa_dic 
# derived from  taxa so that it maps order names to sets of taxa. 
# E.g. 'Chiroptera' : set(['Myotis lucifugus']) etc. 

# create a function that takes a given input and populate the dictionary
def Convert(t, d): 
    for t, n in t: 
        d.setdefault(n, []).append(t) 
    return d 
      
# initialize a dict
dictionary = {} 
resultDict = Convert(taxa, dictionary) 
print (resultDict) 