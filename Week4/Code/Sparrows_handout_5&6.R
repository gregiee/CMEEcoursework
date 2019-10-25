d <- read.table("../Data/SparrowSize.txt", header = TRUE)
# Performing a t-test to see if sample (2001) mean is 18.5
d1<-subset(d,d$Year == 2001)
t.test(d1$Tarsus, mu = 18.5, na.rm=TRUE)
# Show significant. so not equal to 2001

# Using a t-test to test a difference between means (are they equal)

t.test(d1$Tarsus~d1$Sex, na.rm= TRUE)
# Shows not significantly different so can accept H0 that they are the same

#### Handout 5 #######
rm(list = ls())
d <- read.table("../Data/SparrowSize.txt", header = TRUE)
boxplot(d$Mass~d$Sex.1, col = c("red","blue"), ylab = "Body mass (g)") # visualise the difference 

t.test1 <- t.test(d$Mass~d$Sex.1)
t.test1
# shows significantly different
d1 <- as.data.frame(head(d,50))
length(d1$Mass)

t.test2 <- t.test(d1$Mass~d1$Sex)
t.test2
# shows not significantly differenet. Not small sample size

#### Exercise #####
#Test if mean wing length in 2001 is significantly different than overall length
d2 <- subset(d, d$Year==2001)
t.test3 <- t.test(d2$Wing, mu = mean(d$Wing, na.rm =TRUE), na.rm=TRUE)
t.test3
# Not significantly different

# Test if male and female wing lengths differ in 2001
d2m <- subset(d2, d2$Sex.1 == "male")
d2f <- subset(d2, d2$Sex.1 == "female")
t.test4 <- t.test(d2m$Wing, d2f$Wing, na.rm=TRUE)
t.test4
# Significantly different

# Test if overall male and female wing lengths differ
dm <- subset(d, d$Sex.1 == "male", na.rm=TRUE)
df <- subset(d, d$Sex.1 == "female", na.rm = TRUE)
t.test5 <- t.test(dm$Wing, df$Wing , na.rm = TRUE)
t.test5
# Note use comma when lookign at different collumns, a ~ when looking at different factors
# Significantly different
library(reshape2)

##### Lecture 6 #####
library(pwr)
pwr.t.test(d=(0-01.6)/0.96, power = 0.8,sig.level = 0.05, type= "two.sample", alternative = "two.sided")
# to calculate power 
# means of two groups are 0 and 0.16, sd of combined groups are 0.96
# power level 80%


### Run a power analysis to find out how large a sample of winglength data
# must be to detect a difference of an effect size of 5mm
sd_whole <- sd(d$Wing, na.rm = TRUE)
pwr.t.test(d=(0-5)/sd_whole, power = 0.8, sig.level = 0.05, type = "two.sample"
           , alternative = "two.sided")
## Need a sample of size 5