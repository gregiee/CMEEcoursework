# Two example sequences to match
# seq2 = "ATCGCCGGATTACGGG"
# seq1 = "CAATTCGGAT"
import sys
import ipdb

# Assign the longer sequence s1, and the shorter to s2
# l1 is length of the longest, l2 that of the shortest

def openFasta(x):
    with open(x,'r') as f:
        fasta = ""
        counter = 0
        for row in f:
            if counter != 0:
                fasta += row.replace("\n","")
            counter += 1
    print(fasta)
    return fasta


def set(f1, f2):
    l1 = len(f1)
    l2 = len(f2)
    if l1 >= l2:
        s1 = f1
        s2 = f2
    else:
        s1 = f2
        s2 = f1
        l1, l2 = l2, l1 # swap the two lengths
    return s1, s2, l1, l2

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

# now try to find the best match (highest score) for the two sequences'
def best(s1, s2):
    s1, s2, l1, l2 = set(s1, s2)
    my_best_align = None
    my_best_score = -1

    for i in range(l1): # Note that you just take the last alignment with the highest score
        z = calculate_score(s1, s2, l1, l2, i)
        if z > my_best_score:
            my_best_align = "." * i + s2 # think about what this is doing!
            my_best_score = z 
    print(my_best_align)
    print(s1)
    print("Best score:", my_best_score)
    return my_best_align, s1, my_best_score

# f = open("../Data/best_align_result.txt","w+")
# f.writelines([my_best_align,s1,"Best score:" + my_best_score])
# f.close() 

def main(argv):
    if len(argv) >= 3:
        fasta1 = openFasta(argv[1])
        fasta2 = openFasta(argv[2])
    else:
        fasta1 = openFasta("../Data/407228326.fasta")
        fasta2 = openFasta("../Data/407228412.fasta")
    my_best_align, s1, my_best_score = best(fasta1, fasta2)    
    with open('../Data/best_align_result_with_fasta.txt','w') as out:
        out.write('{}\n{}\nbest score: {}\n'.format(my_best_align,s1,my_best_score))
    return 0


if (__name__ == "__main__"):
    status = main(sys.argv)
    sys.exit(status)