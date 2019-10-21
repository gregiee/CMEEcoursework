# Author: Yuchen Yang (yy5819@ic.ac.uk)
# Version: 0.0.1
## Clear the directory ##

rm(list=ls())

###############


a <- NA
for (i in 1:10) {
    a <- c(a, i)
    print(a)
    print(object.size(a))
}



a <- rep(NA, 10)

for (i in 1:10) {
    a[i] <- i
    print(a)
    print(object.size(a))
}

