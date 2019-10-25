rm(list=ls())

Data <- read.table("../Data/SparrowSize.txt",header = TRUE)
###### Lecture 9 #######

x <- c(1,2,3,4,8)
y <- c(4,3,5,7,9)
#running a simple linear model
model1 <- (lm(y~x))
model1
#summary of model
summary(model1)
#
anova(model1)
#residuals
resid(model1)
#covarience
cov(x,y)
#variance
var(x)
#plotting the model
plot(y~x)

summary(model1)$coefficients

