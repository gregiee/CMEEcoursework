# Author: Yuchen Yang (yy5819@ic.ac.uk)
# Version: 0.0.1
## Clear the directory ##

rm(list=ls())

###############

# require(ggplot2)
# require(dplyr)
require(plyr)

MyData <- read.csv("../Data/EcolArchives-E089-51-D1.csv")

# found mg in units, covert everything to g
# find and change mg to g
temp1<-subset(MyData, MyData$Prey.mass.unit!="g")
temp1$Prey.mass<-temp1$Prey.mass/1000
temp1$Prey.mass.unit<-"g"
# find all normal entries
temp2<-subset(MyData, MyData$Prey.mass.unit!="mg")
MyData<-rbind(temp2, temp1)
 

# create output dataframe
Output<-ddply(
  MyData, 
  .(Type.of.feeding.interaction, Predator.lifestage, Location), 
  summarize,
  # intercept of lm
  Intercept=summary(lm(MyData$Predator.mass ~ MyData$Prey.mass))$coef[1,1], 
  # slope of lm
  Slope=summary(lm(MyData$Predator.mass ~ MyData$Prey.mass))$coef[2,1],
  # rsquared value
  R.squared=summary(lm(MyData$Predator.mass ~ MyData$Prey.mass))$r.squared,
  # f
  F.Statistic=summary(lm(MyData$Predator.mass ~ MyData$Prey.mass))$fstatistic[1],
  # using f to do overall pvalue
  Overall.Pvalue=pf(summary(lm(MyData$Predator.mass ~ MyData$Prey.mass))$fstatistic[1],
                    summary(lm(MyData$Predator.mass ~ MyData$Prey.mass))$fstatistic[2],
                    summary(lm(MyData$Predator.mass ~ MyData$Prey.mass))$fstatistic[3],
                    lower.tail=F) 
)

write.csv(Output, "../Results/PP_Regress_loc.csv")