# Author: YUchen Yang (yy5819@ic.ac.uk)
# Version: 0.0.1
## Clear the directory ##

rm(list=ls())


args <- commandArgs(T) 
#add empty input handler
if (length(args) == 0){ 
    stop("Please provide a path to file")
}

#functon to calculate tree height
TreeHeight <- function(degrees, distance){
  radians <- degrees * pi / 180
  height <- distance * tan(radians)
  # print(paste("Tree height is:", height))
  return (height)
}

#load input file and calculate tree height
trees <- read.csv(args[1], sep=",")
degrees <- trees[,3]
distance <- trees[,2]
Tree.Height.m <- TreeHeight(degrees,distance)

#add tree height column to original data
trees$Tree.Height.m <- Tree.Height.m

#get file name without jibber jabber
filename= tools::file_path_sans_ext(basename(args[1]))

#making result file name and path
newpath <- paste("../Results/", filename, "_treeheights.csv")

#create new csv
write.csv(trees, file=newpath)