rm(list=ls()) #clear current data

d <- read.table("../Data/SparrowSize.txt",header =TRUE)
str(d) #displays structure of the data
names(d) #displays the column headers of the data
head(d) # displays headers with first 5 rows of data
length(d$Tarsus) # SHows number of entries in the Tarsus column of the data
hist(d$Tarsus)#builds a histogram of Tarsus
require(ggplot2)
p <- ggplot(d,aes(x=Tarsus))+ geom_histogram()

mean(d$Tarsus)
mean(d$Tarsus,na.rm = TRUE) # mean removing the NAs
median(d$Tarsus, na.rm = TRUE)
mode(d$Tarsus)
par(mfrow = c(2,2)) # splits ploting frame into a 2x2 grid
hist(d$Tarsus , breaks = 3 , col ="grey")
hist(d$Tarsus , breaks = 10, col = "grey")
hist(d$Tarsus , breaks = 30 , col = "grey")
hist(d$Tarsus , breaks = 100, col = "grey")
require(modeest)
mlv #estimates mode for continuous data (most likely value)
d2 <- subset(d, d$Tarsus!="NA") # need to remove NAs
length(d$Tarsus)
length(d2$Tarsus)
mlv(d2$Tarsus)
mean(d$Tarsus,na.rm = TRUE)
median(d$Tarsus,na.rm = TRUE)
mlv(d2$Tarsus)
range(d$Tarsus, na.rm = TRUE) # displays smallest and largest value
range(d2$Tarsus, na.rm = TRUE)
sum((d2$Tarsus - mean(d2$Tarsus))^2)/(length(d2$Tarsus)-1) # Variance
sqrt(var(d2$Tarsus)) # standard deviavtion
sqrt(0.74)
sd(d2$Tarsus)

zTarsus <- (d2$Tarsus - mean(d2$Tarsus))/sd(d2$Tarsus) # z values 
var(zTarsus)
sd(zTarsus)
hist(zTarsus)


set.seed(123) # sets a random number seed
znormal <- rnorm(1e+06) # generates a random normal distribution 
hist(znormal, breaks =100)
summary(znormal) # gives summary of the z normal data

qnorm(c(0.025,0.975)) # dispays the entered quantile values for normal distribution
pnorm(.Last.value) # pnorm gives probability, .Last.Value resuses same values as last call

par(mfrow = c(1,2))
hist(znormal, breaks =100)
abline(v = qnorm(c(0.25,0.5,0.75)), lwd = 2) #adds lines (width 2) at quartiles stated
abline(v = qnorm(c(0.025, 0.975)), lwd = 2, lty = "dashed") # adds dashed lines at quatile stated
plot(density(znormal)) # density plot
abline(v = qnorm(c(0.25,0.5,0.75)), col = "grey")
abline(v = qnorm(c(0.025, 0.975)), lty = "dotted", col = "black")
abline(h = 0, lwd = 3, col = "blue") # adds blue line at the bottom
text(2, 0.3, "1.96", col = "red", adj = 0) # adds 1.96 lable in red at specified position
text(-2, 0.3, "-1.96", col = "red", adj = 1)

dev.off() # closes graphics

boxplot(d$Tarsus~d$Sex.1, col = c("red","blue"), ylab="Tarsus length (mm)") 
# box plot seperated in males and females of Tarsus size

#### lecture 3 #####
plot(density(rnorm(10000))) # normal
plot(density(rpois(10000,3))) # poison
plot(density(rbinom(10000,10,0.5))) # binomal 10000 trials, 10 obs, 0.5 prob
plot(density(rexp(10000))) #exponential
plot(density(runif(100000))) #unifrom
hist(d$Tarsus) # normal, slightly negative skew, cts numeric data
hist(d$Bill) # normal, cts numeric data
hist(d$Wing) # normal, negative skew, cts numeric data
hist(d$Mass, breaks = 100) # normal, cts numeric data
hist(d$Sex) # discrete numeric data
#hist(d$Sex.1) # discrete categoric unranked data

######lecture 4 ######
#### Standard error
#### se = (SD^2/n)^0.5 SD = standard deviation, n = sample size

a<- subset(d$Tarsus, d$Tarsus!="NA")
sqrt(var(a)/length(a)) # se of Tarsus (0.0209)


b <- subset(d$Mass, d$Mass!="NA")
sqrt(var(b)/length(b)) # se of Mass (0.0513)

c <- subset(d$Wing, d$Wing!="NA")
sqrt(var(c)/length(c)) # se of Wing (0.0587)

e <- subset(d$Bill, d$Bill!="NA") 
sqrt(var(e)/length(e)) #se of Bill (0.0177)
# ds = subset(d, is.na!=TRUE)
### for just 2001
d1 <- subset(d, d$Year ==2001)

a1 <- subset(d1$Tarsus, d1$Tarsus!="NA")
sqrt(var(a1)/length(a1)) # se of 2001 data Tarsus (0.1031)

b1 <- subset(d1$Mass, d1$Mass!="NA")
sqrt(var(b1)/length(b1)) # se of 2001 data Mass (0.1807)

c1 <- subset(d1$Wing, d1$Wing!="NA")
sqrt(var(c1)/length(c1)) # se of 2001 data Wing (0.2219)

e1 <- subset(d1$Bill, d1$Bill!="NA")
sqrt(var(e1)/length(e1)) # se of 2001 data Bill (0 as all NA)

