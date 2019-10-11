#!/bin/bash
# Author: YY5819@ic.ac.uk
# Script: tabtocsv.sh
# Description: substitute the commas in the files with spaces
#
# Saves the output into a .csv file
# Arguments: 1 -> tab delimited file
# Date: Oct 2019

echo "Creating a space seperated version of $1 ..."
 # % = For a given filename, whatever it might be, keep everything intact up to the .csv at the end, and replace the .csv with following string 
cat $1 | tr -s "," " " >> ${1%.csv}_Converted.txt 
echo "Done!"
exit


