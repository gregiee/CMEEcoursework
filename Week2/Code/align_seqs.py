#!/usr/bin/env python3
"""takes the DNA sequences as an input from a single external file 
and saves the best alignment along with its corresponding score 
in a single text file (your choice of format and file type) to an appropriate location. """

__author__ = 'Yuchen YANG (YY5819@ic.ac.uk)'
__version__ = '0.0.1'

# Two example sequences to match
# seq2 = "ATCGCCGGATTACGGG"
# seq1 = "CAATTCGGAT"

import csv
import ipdb

temp = []
with open('../Data/seq.csv','r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)

    for row in csvreader:
        temp.append(row[1])

csvfile.close()
seq2 = temp[0]
seq1 = temp[1]
# Assign the longer sequence s1, and the shorter to s2
# l1 is length of the longest, l2 that of the shortest

l1 = len(seq1)
l2 = len(seq2)
if l1 >= l2:
    s1 = seq1
    s2 = seq2
else:
    s1 = seq2
    s2 = seq1
    l1, l2 = l2, l1 # swap the two lengths

# A function that computes a score by returning the number of matches starting
# from arbitrary startpoint (chosen by user)
def calculate_score(s1, s2, l1, l2, startpoint):
    """A function that computes a score by returning the number of matches starting from arbitrary startpoint (chosen by user)"""
    matched = "" # to hold string displaying alignements
    score = 0
    for i in range(l2):
        if (i + startpoint) < l1:
            if s1[i + startpoint] == s2[i]: # if the bases match
                matched = matched + "*"
                score = score + 1
            else:
                matched = matched + "-"

    # some formatted output
    print("." * startpoint + matched)           
    print("." * startpoint + s2)
    print(s1)
    print(score) 
    print(" ")

    return score

# Test the function with some example starting points:
# calculate_score(s1, s2, l1, l2, 0)
# calculate_score(s1, s2, l1, l2, 1)
# calculate_score(s1, s2, l1, l2, 5)

# now try to find the best match (highest score) for the two sequences
my_best_align = None
my_best_score = -1

for i in range(l1): # Note that you just take the last alignment with the highest score
    z = calculate_score(s1, s2, l1, l2, i)
    if z > my_best_score:
        my_best_align = "." * i + s2 # adding the format for seq matching
        my_best_score = z 
print(my_best_align)
print(s1)
print("Best score:", my_best_score)

# f = open("../Data/best_align_result.txt","w+")
# f.writelines([my_best_align,s1,"Best score:" + my_best_score])
# f.close() 


# write the result to result folder
with open('../Results/best_align_result.txt','w') as out:
    out.write('{}\n{}\nbest score: {}\n'.format(my_best_align,s1,my_best_score))

