#!/bin/bash
# Author: Yuchen Yang (yy5819@ic.ac.uk)

#check if there's input, if not, run default file
P1=$1   
DEFAULT_P1="../Data/trees.csv"  
if [ "$P1" == "" ]; then  
    echo Running default file: ../Data/trees.csv
    P1=$DEFAULT_P1  
fi  

echo Running R script... 
Rscript get_TreeHeight.R $P1
echo done!

echo Running Python script...
python3 get_TreeHeight.py $P1
echo done!