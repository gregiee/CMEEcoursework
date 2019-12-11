# CMEE 2019 HPC excercises R code HPC run code proforma

rm(list=ls()) # good practice 
source("YY5819_HPC_2019_main.R")
graphics.off()

getsize <- function(iter){
  if (iter%%4==1){
    size=500
  }
  else if (iter%%4==2){
    size=1000
  }
  else if (iter%%4==3){
    size=2500
  }
  else{
    size=5000
  }
  return(size)
}

simulation <- function(iter){
  set.seed(iter)
  size = getsize(iter)
  time_to_run = 690
  output_filename = "YY5819"
  cluster_run(personal_speciation_rate, size, time_to_run, interval_rich=1, interval_oct=(size/10), burn_in_generations=(8*size), output_filename, iter)
}

iter <- as.numeric(Sys.getenv("PBS_ARRAY_INDEX"))
simulation(iter)