# Author: YUchen Yang (yy5819@ic.ac.uk)
# Version: 0.0.1
## Clear the directory ##

rm(list=ls())

###############

require(lattice)
require(plyr)
MyData <- read.csv("../Data/EcolArchives-E089-51-D1.csv")

# draw the first graph
pdf("../Results/Pred_Lattice.pdf")
hist(log(MyData$Predator.mass),
 	main="Histogram for Predator Mass", 
    xlab="logarithms of masses (g)")
dev.off()

# draw the second graph
pdf("../Results/Prey_Lattice.pdf")
hist(log(MyData$Prey.mass),
	main="Histogram for Prey Mass", 
    xlab="logarithms of masses (g)")
dev.off()

# draw the third graph
pdf("../Results/SizeRatio_Lattice.pdf")
hist(log((MyData$Predator.mass) /(MyData$Prey.mass)),
	main="Histogram for Predator/Prey Mass", 
    xlab="logarithms of mass-ratios")
dev.off()

# create dataframe for final output using ddply
# ddply(.data, .variables, .function,)
output <- ddply(MyData, .(Type.of.feeding.interaction), summarise, 
                    mean.mass.pred = mean(Predator.mass), 
                    median.mass.pred = median(Predator.mass), 
                    mean.mass.prey = mean(Prey.mass), 
                    median.mass.prey = median(Prey.mass),
                    mean.PredatorPrey.ratio = mean(log(Predator.mass/Prey.mass)), 
                    median.PredatorPrey.ratio = median(log(Predator.mass/Prey.mass)))

# write outut to csv
write.csv(output,"../Results/PP_Results.csv")
