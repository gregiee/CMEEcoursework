# Author: YUchen Yang (yy5819@ic.ac.uk)
# Version: 0.0.1
# Clear the directory ##

rm(list=ls())

###############


stochrick<-function(p0=runif(1000,.5,1.5),r=1.2,K=1,sigma=0.2,numyears=100) { 
  N<-matrix(NA,numyears,length(p0))
  N[1,]<-p0

  for (pop in 1:length(p0))
  {
    for (yr in 2:numyears)
    {
      N[yr,pop]<-N[yr-1,pop]*exp(r*(1-N[yr-1,pop]/K)+rnorm(1,0,sigma))
    }
  }
  return(N)
}



stochrickvect <- function(p0=runif(1000,.5,1.5),r=1.2,K=1,sigma=0.2,numyears=100) { # Generates 1000 random values between 0.5 and 1.5 for p0 
  #initialize
  N<-matrix(NA,numyears,length(p0)) 
  N[1,]<-p0 
  for (yr in 2:numyears) 
    {
      # get rid of the first for loop and calculate the population size for each row instead of individually
      N[yr,]<-N[yr-1,]*exp(r*(1-N[yr-1,]/K)+rnorm(1,0,sigma))
    }
  return(N)
}

print ("Non-vectorised Stochastic Ricker takes:")
print(system.time(stochrick()))
print ("Vectorised Stochastic Ricker takes:")
print(system.time(stochrickvect()))