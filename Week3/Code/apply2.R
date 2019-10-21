# Author: Yuchen Yang (yy5819@ic.ac.uk)
# Version: 0.0.1
## Clear the directory ##

rm(list=ls())

###############

SomeOperation <- function(v){ # (What does this function do?)
  if (sum(v) > 0){
    return (v * 100)
  }
  return (v)
}

M <- matrix(rnorm(100), 10, 10)
print (apply(M, 1, SomeOperation))

