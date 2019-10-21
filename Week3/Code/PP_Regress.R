# Author: Yuchen Yang (yy5819@ic.ac.uk)
# Version: 0.0.1
## Clear the directory ##

rm(list=ls())

###############

require(ggplot2)
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
 
# create graph
p <- 
  # draw the basics
  ggplot(MyData, aes(x = Prey.mass, y = Predator.mass, col = Predator.lifestage)) + 
  geom_point(shape = 3) + 
  geom_smooth(method = 'lm', fullrange = TRUE) +
  # forms a matrix of panel based on feeding type
  facet_grid(MyData$Type.of.feeding.interaction) +
  # set default scales for continuous x and y aesthetics
  scale_x_log10() + 
  scale_y_log10() +
  # add labels for x and y
  xlab("Prey Mass in grams") + 
  ylab("Predator Mass in grams") +
  #adjust the scale and theme style
  coord_fixed(ratio = .4) +
  guides(colour=guide_legend(nrow=1))+
  theme_bw() +
  theme(legend.position="bottom", 
        legend.title = element_text(face="bold", size=8), 
        legend.text = element_text(size=6), 
        strip.text.y = element_text(size = 7)) 



# save plot
pdf("../Results/PP_Regress.pdf") 
print(p)
dev.off()

# create output dataframe
Output<-ddply(
  MyData, 
  .(Type.of.feeding.interaction, Predator.lifestage), 
  summarize,
  # get intercept of lm
  Intercept=summary(lm(MyData$Predator.mass ~ MyData$Prey.mass))$coef[1,1], 
  # get slope of lm
  Slope=summary(lm(MyData$Predator.mass ~ MyData$Prey.mass))$coef[2,1],
  # get rsquared value
  R.squared=summary(lm(MyData$Predator.mass ~ MyData$Prey.mass))$r.squared,
  # get f
  F.Statistic=summary(lm(MyData$Predator.mass ~ MyData$Prey.mass))$fstatistic[1],
  # using f to do overall pvalue
  Overall.Pvalue=pf(summary(lm(MyData$Predator.mass ~ MyData$Prey.mass))$fstatistic[1],
                    summary(lm(MyData$Predator.mass ~ MyData$Prey.mass))$fstatistic[2],
                    summary(lm(MyData$Predator.mass ~ MyData$Prey.mass))$fstatistic[3],
                    lower.tail=F) 
)

write.csv(Output, "../Results/PP_Regress_Results.csv")