# Author: YUchen Yang (yy5819@ic.ac.uk)
# Version: 0.0.1

## Clear the directory ##

rm(list=ls())

###############

# This function calculates heights of trees given distance of each tree 
# from its base and angle to its top, using  the trigonometric formula 
#
# height = distance * tan(radians)
#
# ARGUMENTS
# degrees:   The angle of elevation of tree
# distance:  The distance from base of tree (e.g., meters)
#
# OUTPUT
# The heights of the tree, same units as "distance"

# load csv data
TreeData <- read.csv("../Data/trees.csv", header = T)

TreeHeight <- function(degrees, distance){
  radians <- degrees * pi / 180
  height <- distance * tan(radians)
  print(paste("Tree height is:", height))
  return (height)
}

#TreeHeight(37, 40)
TreeDataDistance.m <- TreeData[2]
TreeAngle.degree <- TreeData[3]
Tree.Height.m <- vector()
for (i in 1:nrow(TreeData)) {
  Tree.Height.m <- c(Tree.Height.m, TreeHeight(TreeAngle.degree[i,1],TreeDataDistance.m[i,1]))
}
#add height to data
TreeData$Tree.Height.m<-Tree.Height.m

write.csv(TreeData, "../Results/TreeHts.csv")
# This function calculates heights of trees given distance of each tree 
# from its base and angle to its top, using  the trigonometric formula 
#
# height = distance * tan(radians)
#
# ARGUMENTS
# degrees:   The angle of elevation of tree
# distance:  The distance from base of tree (e.g., meters)
#
# OUTPUT
# The heights of the tree, same units as "distance"

# load csv data
TreeData <- read.csv("../Data/trees.csv", header = T)

TreeHeight <- function(degrees, distance){
  radians <- degrees * pi / 180
  height <- distance * tan(radians)
  print(paste("Tree height is:", height))
  
  return (height)
}

#TreeHeight(37, 40)
TreeDataDistance.m <- TreeData[2]
TreeAngle.degree <- TreeData[3]
Tree.Height.m <- vector()

for (i in 1:nrow(TreeData)) {
  Tree.Height.m <- c(Tree.Height.m, TreeHeight(TreeAngle.degree[i,1],TreeDataDistance.m[i,1]))
}
#add height to data
TreeData$Tree.Height.m<-Tree.Height.m

write.csv(TreeData, "../Results/TreeHts.csv")
