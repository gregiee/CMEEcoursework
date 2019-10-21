# Author: Yuchen Yang (yy5819@ic.ac.uk)
# Version: 0.0.1
## Clear the directory ##

rm(list=ls())

###############
i <- 0 #Initialize i
	while(i < Inf) {
		if (i == 10) {
			break 
             } # Break out of the while loop! 
		else { 
			cat("i equals " , i , " \n")
			i <- i + 1 # Update i
	}
}

