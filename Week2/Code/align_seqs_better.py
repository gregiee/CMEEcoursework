#!/usr/bin/env python
"""match two sequences and ouput all best results"""

__author__ = 'Yuchen Yang (yy5819@imperial.ac.uk)'
__version__ = '1.0.0'

import sys
import pickle
import os
import ipdb

# actual input files
# find the inputfile name and read the sequences
if len(sys.argv) > 1:
    File1_direction = r'../Data/' + sys.argv[1]
    File2_direction = r'../Data/' + sys.argv[2]
else:  # using seq1.csv and seq2.csv as default input
    File1_direction = r'../Data/407228326.fasta'
    File2_direction = r'../Data/407228412.fasta'

# re-used the function to deal with fasta file
def openFasta(x):
    with open(x,'r') as f:
        fasta = ""
        counter = 0
        for row in f:
            if counter != 0:
                fasta += row.replace("\n","")
            counter += 1
    # print(fasta)
    return fasta

seq1 = openFasta(File1_direction)
seq2 = openFasta(File2_direction)

# # test seqs
# seq1 = "AC"
# seq2 = "TGACCGACGGACACAGGAC"

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
    matched = "" # to hold string displaying alignements
    score = 0
    for i in range(l2):
        if (i + startpoint) < l1:
            if s1[i + startpoint] == s2[i]: # if the bases match
                matched = matched + "*"
                score = score + 1
            else:
                matched = matched + "-"

    # # some formatted output
    # print("." * startpoint + matched)           
    # print("." * startpoint + s2)
    # print(s1)
    # print(score) 
    # print(" ")

    return score

# Test the function with some example starting points:
# calculate_score(s1, s2, l1, l2, 0)
# calculate_score(s1, s2, l1, l2, 1)
# calculate_score(s1, s2, l1, l2, 5)

# now try to find the best match (highest score) for the two sequences
my_best_align = None
my_best_score = -1
best_results=[]
#if want to use pickle uncomment the best_Result as dict
# best_result={}

# running through to get the highest score
for i in range(l1): 
    z = calculate_score(s1, s2, l1, l2, i)
    if z >= my_best_score:
        my_best_score = z 

# write all hightest score to a file
with open('../Results/all_best_align_results.txt','w') as f:
    for i in range(l1):
        z = calculate_score(s1, s2, l1, l2, i)
        if z == my_best_score:
            my_best_align = "." * i + s2 # adding the format for seq matching
            best_results.append((my_best_align,s1,my_best_score))
            print("writing to result txt files",my_best_align,s1,my_best_score)
            f.write('\n\nbest result:\n{}\n{}\nscore: {}\n'.format(my_best_align,s1,my_best_score))
    f.close()


# # comment out the populate pickle script
# f = open('../Results/all_best_align_results.p','wb') ## note the b: accept binary files
# pickle.dump(best_results, f)
# f.close()

# # comment out the load pick to dict test
# t = open('../Results/all_best_align_results.p','rb')
# test_load_dict = pickle.load(t)
# print(test_load_dict)
# t.close()