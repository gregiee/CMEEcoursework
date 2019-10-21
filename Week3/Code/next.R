# Author: Yuchen Yang (yy5819@ic.ac.uk)
# Version: 0.0.1
## Clear the directory ##

rm(list=ls())

###############
for (i in 1:10) {
  if ((i %% 2) == 0) 
    next # pass to next iteration of loop 
  print(i)
}