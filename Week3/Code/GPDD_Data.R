# Author: Yuchen Yang (yy5819@ic.ac.uk)
# Version: 0.0.1
## Clear the directory ##

rm(list=ls())

###############

# required packages
require(maps)

# load data
load("../Data/GPDDFiltered.RData")
gpdd <- as.data.frame(gpdd)

# initiate the map
map(database = "world", fill = T, col=rgb(.2,.3,.5,.5))

# draw points
points(x = gpdd$long, y = gpdd$lat, pch = 20)


#Biases 
#1
#the data covers north america and europe, 
#but not other contries(except for rare data entries in japan and africa)
#2
#the data is mainly terrestrial
#3
#the data focuses mainly on the north sphere 

