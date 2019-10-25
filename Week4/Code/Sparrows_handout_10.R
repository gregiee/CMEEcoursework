rm(list=ls())
#import data
d <- read.table("../Data/SparrowSize.txt", header = TRUE)
# plot data interested in
plot(d$Mass~d$Tarsus, ylab = "Mass (g)",
     xlab = "Tarsus (mm)", pch =19, cex = 0.4)
#plot a simple linear line
x <- c(1:100)
b <- 0.5
m <- 1.5
y <- m*x+b
plot(x,y, xlim=c(0,100), ylim=c(0,100), pch=19, cex=0.5)
# inspect mass data
d$Mass
length(d$Mass)
d$Mass[1770]
# plot data again
plot(d$Mass~d$Tarsus, ylab="Mass (g)", xlab = "Tarsus (mm)",
     pch = 19, cex = 0.4, ylim=c(-5,38), xlim = c(0,22))
# # remove NA's
d1 <- subset(d, d$Mass!="NA")
d2 <- subset(d1, d1$Tarsus!="NA")
# create linear model of subsetted data
model1 <- lm(Mass~Tarsus, data = d2)
# summarize the model
summary(model1)
#plot the residuals
hist(model1$residuals)
#view residuals
head(model1$residuals)

# create a second linear model of straight line
model2<-lm(y~x)
summary(model2)

# run model of z-scores
d2$z.Tarsus <- scale(d2$Tarsus)
model3<- lm(Mass~z.Tarsus, data = d2)
summary(model3)

#plotting results
plot(d2$Mass~d2$z.Tarsus, pch = 19, cex = 0.4)
abline(v=0, lty = "dotted") # plot x axis

#inspect data
head(d)
str(d)


d$Sex <- as.numeric(d$Sex) #change sex to 0 or 1 so can plot
par(mfrow=c(1,2)) # seperate plot area
plot(d$Wing~d$Sex.1, ylab= "Wing(mm)") # plot box plot of sex vs Wing length
plot(d$Wing~d$Sex, xlab="Sex", xlim=c(-0.1,1.1), ylab = " ") # Plot numerical sex against Wing length
abline(lm(d$Wing~d$Sex), lwd =2) # Add a regression line of the linear model
text(0.15,76,"intercept") # annotate the intercept
text(0.9,77.5,"slope", col = "red") # annotate the slope


d4 <- subset(d, d$Wing!="NA")
m4 <- lm(Wing~Sex, data = d4)
t4 <- t.test(d4$Wing~d4$Sex, var.equal=TRUE)
summary(m4)

par(mfrow=c(2,2))
plot(model3)

par(mfrow=c(2,2))
plot(m4)
##### JUST NEED EXERCISES AT THE END #####
