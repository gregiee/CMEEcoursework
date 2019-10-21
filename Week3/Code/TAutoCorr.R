# Author: Yuchen Yang (yy5819@ic.ac.uk)
# Version: 0.0.1
## Clear the directory ##

rm(list=ls())

###############

# load in the data
# print(load("../Data/KeyWestAnnualMeanTemperature.RData")) to get the var name "ats"
load("../Data/KeyWestAnnualMeanTemperature.RData")
# get entries count 
b <- dim(ats)[1]

# assign 1-99, 2-100 data entry to two different vars
c1 <- ats[1:b-1,2]
c2 <- ats[2:b,2]
# calculate the correlation
Ori_Cor <- cor(c1,c2)

# generate a 10000 array with NAs
sample_r <- rep(NA,10000)

# calculate the correlation of 10000 samples and store it
for (i in 1:10000){
  s <- sample(ats[,2],b)
  t1 <- s[1:b-1]
  t2 <- s[2:b]
  sample_r[i] <- cor(t1,t2)
}

# calculate the pvalue
p_value <- length(sample_r[sample_r>Ori_Cor]) / length(sample_r)
print(p_value)

# draw the plot
plot.new()

pdf("../Results/TAutoCorr_graph.pdf") # Open blank pdf page using a relative path
#draw histogram for the samples
hist(
	sample_r, 
	freq = TRUE,
	main = "Temperature Coefficients histagram",
	xlab = "correlation coefficient values", 
	ylab = "Frequency", 
	col = rgb(.8,.2,.4), 
	breaks = 30
	) 

# draw line for original data
abline(
	v = Ori_Cor, # v is to set the xvalue for the abline, draw the original cor on the graph
	lwd = 2
	) 
# draw legend for both data
legend(
	'topleft', 
	c("10000 random samples", "original successive year"),
	fill = c(rgb(.8,.2,.4), rgb(0, 0, 0)),
	cex = .7
	)

dev.off()

