# Author: Yuchen Yang (yy5819@ic.ac.uk)
# Version: 0.0.1
## Clear the directory ##

rm(list=ls())

###############

## Build a random matrix
M <- matrix(rnorm(100), 10, 10)

## Take the mean of each row
RowMeans <- apply(M, 1, mean)
print (RowMeans
## Now the variance
RowVars <- apply(M, 1, var)
print (RowVars)
## By column
ColMeans <- apply(M, 2, mean)
print (ColMeans)
