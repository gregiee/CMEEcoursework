rm(list = ls())

daphina <- read.delim("../Data/daphnia.txt")
summary(daphina) # quick look at data

### check for outliers

par(mfrow =c(1,2))
plot(Growth.rate ~ Detergent , data = daphina)
plot(Growth.rate ~ Daphnia, data = daphina)
# no outliers

require(dplyr) # load package

### summarise the Gorwth rates by Detergent
daphina %>%
  group_by(Detergent) %>%
  summarise(variance = var(Growth.rate))

### summarise the Growth rates by Daphnia
daphina %>%
  group_by(Daphnia) %>%
  summarise(variance=var(Growth.rate))


#### Is the data normally distributed
hist(daphina$Growth.rate)

# Judging by histogram not excessively many zeros
# Collinearity of the covariates doesn't apply here as
# only have catergories
# Previous boxplots suitable way to visually inspect 
# relationships
# Don't need to consider interactions here

