# CMEE 2019 HPC excercises R code main proforma
# you don't HAVE to use this but it will be very helpful.  If you opt to write everything yourself from scratch please ensure you use EXACTLY the same function and parameter names and beware that you may loose marks if it doesn't work properly because of not using the proforma.

name <- "Yuchen Yang"
preferred_name <- "Yuchen"
email <- "yuchen.yang19@imperial.ac.uk"
username <- "yy5819"
personal_speciation_rate <- 0.003085 # will be assigned to each person individually in class and should be between 0.002 and 0.007

# Question 1
species_richness <- function(community){
  # Calculate community species richness
  return(length(unique(community))) 
}

# Question 2
init_community_max <- function(size){
  # Initial community, maximum richness=size
  return(seq(size))
}

# Question 3
init_community_min <- function(size){
  # Initial community with minimum richness=1
  return(rep(1,size))
}

# Question 4
choose_two <- function(max_value){
  # Choose 2 individuals in community randomly 
  return(sample(max_value,2))
}

# Question 5
neutral_step <- function(community){
  # A neutral model simulation without speciation
  # kills one individual and allows another to replace it.
  dieRep=choose_two(length(community))
  community[dieRep[1]]=community[dieRep[2]]
  return(community)
}

# Question 6
neutral_generation <- function(community){
  # Simulate neutral_steps in a community to pass a gen
  times=round(length(community)/2)
  for (i in 1:times){
    community=neutral_step(community)
  }
  return(community)
  
}

# Question 7
neutral_time_series <- function(community,duration)  {
  richness_ser = rep(species_richness(community),duration+1)
  for (i in 1:duration){
    community = neutral_generation(community)
    richness_ser[i+1] = species_richness(community)
  }
  return(richness_ser)
}

# Question 8
question_8 <- function() {
  # plot a time seriesof neutral model species richness
  # clear any existing graphs and plot your graph within the R window
  while (!is.null(dev.list()))  dev.off()
  y = neutral_time_series(init_community_max(100),duration=200)
  plot(1:length(y), y, xlab="Generations", ylab = "Species Richness", cex=0.8, pch=20,
       main="Netural Model Species Richness Over Time Series")
  return("Population will converge to 1 species under this setting given enough time. 
          Because when no new species could enter the pop, one lost is permanent. 
          And over time only one remains due to random loss.")
}

# Question 9
neutral_step_speciation <- function(community,speciation_rate)  {
  # One step of a zero sum neutral model with a chance for speciation
  r=runif(1)
  dieRep=choose_two(length(community))
  die=dieRep[1]
  if (r > speciation_rate){
    community[dieRep[1]] <- community[dieRep[2]]
  }
  else{
    community[dieRep[1]] <- max(community)+1
  }
  return(community)
  
}

# Question 10
neutral_generation_speciation <- function(community,speciation_rate)  {
  # One generation of a zero sum neutral model with a chance for speciation
  time=round(length(community)/2)
  for (i in 1:time){
    community=neutral_step_speciation(community,speciation_rate)
  }
  return(community)
}

# Question 11
neutral_time_series_speciation <- function(community,speciation_rate,duration)  {
  # the species richness of (duration) generations of a zero sum neutral model with a chance for speciation
  richSer = rep(species_richness(community),duration+1)
  for (i in 1:duration){
    community = neutral_generation_speciation(community,speciation_rate)
    richSer[i+1] = species_richness(community)
  }
  return(richSer)
}

# Question 12
question_12 <- function()  {
  # Neutral model with speciation, from both an initial max and minimum species richness.
  # clear any existing graphs and plot your graph within the R window
  while (!is.null(dev.list()))  dev.off()
  dMax = neutral_time_series_speciation(init_community_max(100), 0.1, 200)
  dMin = neutral_time_series_speciation(init_community_min(100), 0.1, 200)
  plot(seq(length(dMax)), dMax, xlab="Generations", ylab="Species Richness", ylim=c(0,100),
          main="Neutral Model Simulation with Speciation (v=0.1)", type="l", col="blue", cex.lab=1.6, cex.axis=1.6, cex.main=1.6, cex.sub=1.6)
  lines(seq(length(dMax)), dMin, col="red")
  legend(70, 70,legend=c("Max initial richness", "Min initial richness"), col=c("blue", "red"), lty=1:2, cex=1.2)
  return("The neutral model comes down to same species richness value regardless of initial conditions. 
  Species richness at equilibrium is dictated by the point where Rspeciation matches Rspecies-lost.
  Initial species richness only affects the behaviour of the begining.")
}

# Question 13
species_abundance <- function(community)  {
  # Claculate species abundance
  return(sort(as.numeric(table(community)),decreasing=T))
}

# Question 14
octaves <- function(abundance_vector) {
  # Abundance vector -> octave bins based on log2
  return(tabulate(floor(log2(abundance_vector)+1)))
}

# Question 15
sum_vect <- function(x, y) {
  # Sum length-different vectors
  xlen=length(x)
  ylen=length(y)
  if (ylen>xlen){
    z=x
    x=y
    y=z
  }
  x[1:length(y)]=x[1:length(y)]+y
  return(x)
}

# Question 16 
question_16 <- function()  {
  # Generate octaves for mean species richness at equilibrium and plot
  # clear any existing graphs and plot your graph within the R window
  while (!is.null(dev.list()))  dev.off()
  community=init_community_max(100)   
  speciation_rate=0.1
  burnin=200
  duration=2000
  per=20
  for (i in 1:burnin){
    community <- neutral_generation_speciation(community, speciation_rate) # Runs one generation's changes
  }
  vect<- octaves(species_abundance(community))
  vect_mean=1
  for (i in 1:duration){
    community <- neutral_generation_speciation(community, speciation_rate)
    if (i %% per == 0){
      vect<-sum_vect(vect, octaves(species_abundance(community)))
      vect_mean=vect_mean+1
    }
  }
  vect<-vect/vect_mean
  names(vect)<- (seq(length(vect)))
  barplot(vect, xlab = "Abundance", main="Abundance Octaves (J=100)", ylab="Number of Species", ylim=c(0, 10), cex.lab=1.6, cex.axis=1.6, cex.main=1.6, cex.sub=1.6)
  return("Initial condition does not matter.
  Values are measured after a dynamic equilibrium is reached by the simulation.
  Question 12 illustrate why the dynamic equilibrium is not affected by initial species richness.")
}

# Question 17
cluster_run <- function(speciation_rate, size, wall_time, interval_rich, interval_oct, burn_in_generations, output_file_name, iter)  {
  tic=proc.time()
  community=init_community_min(size)
  richness=c(species_richness(community))
  oct=c(list(octaves(species_abundance(community))))
  generation=0
  while(as.numeric(proc.time()-tic)[3] < (wall_time *60)){
    community=neutral_generation_speciation(community, speciation_rate)
    generation = generation+1
    if ((generation <= burn_in_generations) & (generation%%interval_rich==0)){
      richness = c(richness, species_richness(community))
    }
    if (generation%%interval_oct==0){
      oct=c(oct,list(octaves(species_abundance(community))))
    }
  }
  totaltime=as.numeric(proc.time()-tic)[3]
  save(totaltime,speciation_rate,size,wall_time,interval_rich,interval_oct,burn_in_generations,community, richness, oct, file = paste(output_file_name, "_", iter, ".rda", sep = ""))
}

# Questions 18 and 19 involve writing code elsewhere to run your simulations on the cluster

# cluster_run(speciation_rate=0.1, size=100, wall_time=1, interval_rich=1, interval_oct=10, burn_in_generations=200, output_file_name='../Results/YY5819',8)
# Question 20 
process_cluster_results <- function (iter=100){
  # Create empty lists for later use
  finalOcts=list()
  Vect_mean=list()
  for (i in 1:iter){ #Loop over each of the 100 runs
    f = paste("../Results/rda/YY5819_",i,".rda", sep="")
    load(f) #Load the RData file for each iteration
    #print(f)
    if (is.null(finalOcts[[as.character(size)]])){ #Runs if no runs for that J have been recorded
      print(burn_in_generations)
      print(length(oct))
      startpoint = burn_in_generations/interval_oct
      finalOcts[[as.character(size)]]<-oct[[startpoint]] #Places the first octaves from this run into finalOcts per J
      Vect_mean[[as.character(size)]]<-length(oct)-startpoint #Records how many octaves were measured for this run
      for (j in (startpoint+1):length(oct)){
        # Sums all recorded octaves for that run
        finalOcts[[as.character(size)]]<-sum_vect(finalOcts[[as.character(size)]], oct[[j]])
      }
    }
    else{ # If at least one run for that J has already been recorded
      # Adds to tot. number of recorded octaves for that J
      Vect_mean[[as.character(size)]]<-Vect_mean[[as.character(size)]]+(length(oct)-startpoint)
      for (j in (startpoint+1):length(oct)){
        # Sums recorded octaves for that run with total so far from other runs
        finalOcts[[as.character(size)]]<-sum_vect(finalOcts[[as.character(size)]], oct[[j]])
      }
    }
  }
  Sizes=names(finalOcts) # Records size names for graph
  par(mfrow=c(2,2),oma=c(0,0,2,0))
  final=list() 
  for (i in 1:length(Sizes)){ # For each value of J
    names(finalOcts[[i]])<- 2^(seq(length(finalOcts[[i]]))) # Names the octave bins
    final[[i]]<-finalOcts[[i]]/Vect_mean[[i]] # Generates the mean octave
    # Makes a barplot of the abundance octaves
    p <- barplot(final[[i]], main=paste("Community size =  ", Sizes[i]), xlab = "Number of Individuals/Species", ylab="Number of Species")
    title("Average Species Abundance", outer=TRUE)
    p
  }
  #print(final)
  save(final, file="../Results/YY5819_cluster_results.rda")
  return(final)

}

# Question 21
question_21 <- function()  {
  f<- log(8,10)/log(3,10)
  e<-"tripling the size the object requires 8 times as many of the original, dimension of fractal = log8/log3" 
  answer<-c(f,e)
  return(answer)
}

# Question 22
question_22 <- function()  {
  f<- log(20,10)/log(3,10)
  e<-"tripling the size the object requires 20 times as many of the original, dimension of fractal = log20/log3" 
  answer<-c(f,e)
  return(answer)
}

# Question 23
chaos_game <- function()  {
  # clear any existing graphs and plot your graph within the R window
  while (!is.null(dev.list()))  dev.off()
  A = c(0,0)
  B = c(3,4)
  C = c(4,1)
  P = list(A,B,C)
  move_point = A
  plot(0:10,0:10, type = "n")
  points(x = move_point[1],y= move_point[2], cex = 0.2)
  for (i in (1:20000)) {
    direc = unlist(sample(P,1))
    move_point = c(((move_point[1] + direc[1])/2), ((move_point[2] + direc[2])/2))
    points(x = move_point[1], y = move_point[2], cex = 0.2)
  }
  return("the function generate a triangle fractal.")
}

# Question 24
turtle <- function(start_position = c(2,2), direction = pi/2, length = 1)  {
  angle = direction
  y = cos(angle)*length
  x = sin(angle)*length
  segments(start_position[1], start_position[2], x+start_position[1], y+start_position[2])
  return(c(x+start_position[1],y+start_position[2]))
}

# Question 25
elbow <- function(start_position = c(2,2), direction = pi/2, length = 1)  {
  P1 = turtle(start_position, direction, length)
  P2 = turtle(c(P1), direction+(pi/4), 0.95*length)
}

# Question 26
spiral <- function(start_position = c(2,2), direction = pi/2, length = 1)  {
  if (length > 0.2){
    P1 = turtle(start_position, direction, length)
    P2 = spiral(c(P1), direction+(pi/4), 0.95*length)
    return("Would arise error too close to the limit.
           It keeps drawting smaller lengths Resulting in a infinite loop")
  }
}

# Question 27
draw_spiral <- function(start_position = c(2,2), direction = pi/2, length = 1)  {
  # clear any existing graphs and plot your graph within the R window
  while (!is.null(dev.list()))  dev.off()
  plot(0:10,0:10, type = "n")
  P1 = turtle(start_position, direction, length)
  spiral(c(P1), direction+(pi/4), 0.95*length)
}

# Question 28
tree <- function(start_position, direction, length)  {
  if (length > 0.01){
    P1 = turtle(start_position, direction, length)
    P2 = tree(c(P1), direction+(pi/4), 0.65*length)
    P3 = tree(c(P1), direction-(pi/4), 0.65*length)
    return("Would arise error too close to the limit.
           It keeps drawting smaller lengths Resulting in a infinite loop")
  }
}
draw_tree <- function(start_position = c(2,2), direction = 2*pi, length = 1)  {
  # clear any existing graphs and plot your graph within the R window
  while (!is.null(dev.list()))  dev.off()
  plot(0:10, 0:10, type = "n")
  tree(start_position, direction, length)
}

# Question 29
fern <- function(start_position, direction, length)  {
  if (length > 0.01){
    P1 = turtle(start_position, direction, length)
    P2 = fern(c(P1), direction-(pi/4), 0.38*length)
    P3 = fern(c(P1), direction, 0.87*length) 
    return("Would arise error too close to the limit.
           It keeps drawting smaller lengths Resulting in a infinite loop")
  }
}
draw_fern <- function(start_position = c(2,2), direction = 2*pi, length = 0.7)  {
  # clear any existing graphs and plot your graph within the R window
  while (!is.null(dev.list()))  dev.off()
  plot(0:10,0:10, type = "n")
  fern(start_position, direction, length) 
}

# Question 30
fern2 <- function(start_position, direction, length, dir)  {
  if (length > 0.005){
    P1 = turtle(start_position, direction, length)
    if (dir==-1){
      P2 = fern2(c(P1), direction-(pi/4), 0.38*length, dir=-1)
      P3 = fern2(c(P1), direction, 0.87*length, dir=1) 
    }
    else if (dir==1){
      P2 = fern2(c(P1), direction+(pi/4), 0.38*length, dir=1)
      P3 = fern2(c(P1), direction, 0.87*length, dir=-1) 
    } 
    return("Would arise error too close to the limit.
           It keeps drawting smaller lengths Resulting in a infinite loop")
  }
}
draw_fern2 <- function(start_position = c(2,2), direction = 2*pi, length = .7, dir = -1)  {
  # clear any existing graphs and plot your graph within the R window
  while (!is.null(dev.list()))  dev.off()
  plot(0:10,0:10, type = "n")
  fern2(start_position, direction, length, dir)
}

# Challenge questions - these are optional, substantially harder, and a maximum of 16% is available for doing them.  
# Challenge question A
Challenge_A <- function(duration=200,v=0.1,size=100,alpha=1-0.972,iter=30) {
  # clear any existing graphs and plot your graph within the R window
  while (!is.null(dev.list()))  dev.off()
  n=duration+1
  richMin=replicate(iter, neutral_time_series_speciation(init_community_min(size),v,duration))
  richMax=replicate(iter, neutral_time_series_speciation(init_community_max(size),v,duration))
  #mean
  richMin_mean=apply(richMin,1,mean)
  richMax_mean=apply(richMax,1,mean)
  #sd
  richMin_sd=apply(richMin,1,sd)
  richMax_sd=apply(richMax,1,sd)
  #CI
  CI_min=richMin_sd/sqrt(n)*qt(1-alpha/2,df=iter-1)
  CI_max=richMax_sd/sqrt(n)*qt(1-alpha/2,df=iter-1)
  CI=data.frame(minMean=richMin_mean,
                minTop=richMin_mean+CI_min,
                minBtm=richMin_mean-CI_min,
                maxMean=richMax_mean,
                maxTop=richMax_mean+CI_max,
                maxBtm=richMax_mean-CI_max,
                stringsAsFactors = TRUE)
  par(mfrow=c(1,2))
  plot(CI$minMean, xlab = "Generation time", ylab = "Mean Species richness", main = "Richness Over Time\ninitialise_max",
       col = "red", type = "l", ylim = range(0,100))
  segments(c(1:n),CI$minBtm,c(1:n),CI$minTop,col="green")   #add confidence interval
  plot(CI$maxMean, xlab = "Generation time", ylab = "Mean Species richness", main = "Richness Over Time\ninitialise_min",
       col = "red", type = "l", ylim = range(0,100))
  segments(c(1:n),CI$maxBtm,c(1:n),CI$maxTop,col="green")
  mtext("Confidence interval = 97.2%",side=4)
}


# Challenge question B
calRichness <- function(initial, v, rep, duration){
  # Initialises empty vectors
  richness<-integer(duration+1)
  sumRich<- integer(duration+1)
  for (i in 1:(rep)){ # Repeats rep times
    # Runs one time series and generates vector of richness over time
    timeS=neutral_time_series_speciation(initial, v, duration)
    richness=sum_vect(richness, timeS) #Adds time series to Rich
    sumRich=sum_vect(sumRich, (timeS)^2) # Adds Richness^2 for later calculation of varience
  }
  out=list(richness, sumRich) # Creates a list so both vectors can be returned
  return(out)
}
challenge_B <- function(pop=100, v=0.1, iter=10, duration=200){
  # Initialises an empty plot with all nessecary labels
  plot(x=NULL, ylim=c(0,100), xlim=c(0,duration), xlab="Generations", main="Mean Species Richness over time", 
          ylab="Mean Species Richness", cex.lab=1.6, cex.axis=1.6, cex.main=1.6, cex.sub=1.6)
  allRichness=c() # Initialises empty vector
  for (i in 1:pop){
    #Ensures that this value of species richness can have equal numbers of each species
    if (pop %% i == 0){ 
      run_rich=100/i
      initial=rep(seq(1,i), run_rich) # Generates a vector of size pop with equal numbers of each species
      # Runs the add-on function to calculate richness over time
      sumRich=calRichness(initial, v, iter, duration)
      rich_mean=sumRich[[1]]/iter # Generates mean richness
      allRichness=c(allRichness, i) # Stores the initial richness value
      # Plots the species richness over time, with a colour determined by picking from a rainbow sequence
      lines(rich_mean, type="l", col=rainbow(9)[tail(seq(1,length(allRichness)), n=1)])
    }
    else{
      next()
    }
  }
  # Adds a legend to the plot using the stored use_rich values and rainbow colours
  legend(150,100,legend=allRichness,lty=1,col=rainbow(9)[seq(1,length(allRichness))], title="Species Richness")
}


# Challenge question C
Challenge_C <- function(iter=100) {
  # clear any existing graphs and plot your graph within the R window
  while (!is.null(dev.list()))  dev.off()
  par(mfrow=c(2,2))
  richness500 = c(0)
  richness1000 = c(0)
  richness2500 = c(0)
  richness5000 = c(0)
  
  for (i in (1:iter)){
    f = paste("../Results/rda/YY5819_",i,".rda",sep = "")
    load(f)
    if(i%%4==1){
      richness500 = sum_vect(richness500, richness)
    }
    else if(i%%4==2){
      richness1000 = sum_vect(richness1000, richness)
    }
    else if(i%%4==3){
      richness2500 = sum_vect(richness2500, richness)
    }
    else{
      richness5000 = sum_vect(richness5000, richness)
    }
  }
  
  ave500 = richness500/(iter/4)
  rmax500 = max(ave500)
  
  ave1000 = richness1000/(iter/4)
  rmax1000 = max(ave1000)
  
  ave2500 = richness2500/(iter/4)
  rmax2500 = max(ave2500)
  
  ave5000 = richness5000/(iter/4)
  rmax5000 = max(ave5000)
  
  plot(c(0,1000), c(0, rmax500*1.3), type = "n",
       xlab = "Generation", ylab = "Species Richness",
       main = "Average Species Richness Over Time. \nSize:500")
  lines(seq(0,(8*500)), ave500, col = "black")
  abline(v=250)
  plot(c(0,1000), c(0,rmax1000*1.3), type = "n",
       xlab = "Generation", ylab = "Species Richness",
       main = "Average Species Richness Over Time. \nSize:1000")
  lines(seq(0,(8*1000)), ave1000, col = "red")
  abline(v=300)
  plot(c(0,1000), c(0,rmax2500*1.3), type = "n",
       xlab = "Generation", ylab = "Species Richness",
       main = "Average Species Richness Over Time. \nSize:2500")
  lines(seq(0,(8*2500)), ave2500, col = "green")
  abline(v=500)
  plot(c(0,1000), c(0,rmax5000*1.3), type = "n",
       xlab = "Generation", ylab = "Species Richness",
       main = "Average Species Richness Over Time.  \nSize:5000")
  lines(seq(0,(8*5000)), ave5000, col = "blue")
  abline(v=400)
}

# Challenge question D
Challenge_D <- function() {
  # clear any existing graphs and plot your graph within the R window
  while (!is.null(dev.list()))  dev.off()
  calAbund<- function(community, speciationRate){
    lin = init_community_min(community)
    abund = c()
    N = community
    theta = speciationRate*(community-1)/(1-speciationRate)
    
    while (N > 1){
      j = choose_two(length(lin))
      randnum = runif(1)
      
      if (randnum < theta/(theta+N-1)){
        abund = c(abund, lin[j[1]])
      }
      else lin[j[2]] = (lin[j[2]] + lin[j[1]])
      lin = lin[-j[1]]
      N = N-1
    }
    abund = c(abund, lin)
    return (abund)
  }
  runSim <- function(iter=100){
    sum500 = c(0)
    sum1000 = c(0)
    sum2500 = c(0)
    sum5000 = c(0)
    for (i in 1:iter){
      sum2500 = sum_vect(sum2500, octaves(calAbund(2500, personal_speciation_rate)))
      sum1000 = sum_vect(sum1000, octaves(calAbund(1000, personal_speciation_rate)))
      sum500 = sum_vect(sum500, octaves(calAbund(500, personal_speciation_rate)))
    }
    tick = proc.time()[3]
    for (i in 1:iter){
      sum5000 = sum_vect(sum5000, octaves(calAbund(5000, personal_speciation_rate)))
    }
    tock = proc.time()[3]
    ave500 = sum500/(iter/4)
    ave1000 = sum1000/(iter/4)
    ave2500 = sum2500/(iter/4)
    ave5000 = sum5000/(iter/4)
    
    par(mfrow = c(2,2),oma=c(0,0,2,0))
    barplot(ave500, names.arg = c(2^((1:length(ave500))-1)),
            main = "Size:500",
            xlab = "Generation", ylab = "Species Richness")
    barplot(ave1000, names.arg = c(2^((1:length(ave1000))-1)),
            main = "Size:1000",
            xlab = "Generation", ylab = "Species Richness")
    barplot(ave2500, names.arg = c(2^((1:length(ave2500))-1)),
            main = "Size:2500",
            xlab = "Generation", ylab = "Species Richness")
    barplot(ave5000, names.arg = c(2^((1:length(ave5000))-1)),
            main = "Size:5000",
            xlab = "Generation", ylab = "Species Richness")
    title("Average Species Richness Over Time.", outer=TRUE)
    
    run_time = as.numeric(tock - tick)
    print (paste("coalescence theory spent time for 100 size5000 simulation: ", run_time, "s"))
  }
  
  cluster_time <- function(){
    total_t = 0
    for (i in 1:100){
      f = paste("../Results/rda/YY5819_",i,".rda",sep = "")
      load(f)
      total_t = total_t + totaltime
    }
    
    print (paste("cluster spent time for ~1300 size5000 simulations: ", totaltime, "s"))
  }
  runSim()
  cluster_time()
  return("as seen in the previous run time comparision, the coalescence simulaiton is much faster.
  coalescence simulation is faster since it only take lineages that stayed are tracked.
  on contrary, the forward based model simulated lineages are eventually extincted, which wasted time. 
  the burn-in period for the time-series model is not required for coalescence model.
  since when lineages stayed till the end, it is known that the community was at equilibrium.")
}

# Challenge question E
Challenge_E <- function() {
  # clear any existing graphs and plot your graph within the R window
  while (!is.null(dev.list()))  dev.off()
  par(mfrow=c(2,3))
  e1 <- function(xpoints, ypoints, init, dis){
    points(init[1], init[2], cex = 0.5, col = "red")
    for (i in 1:7000) {
      n=sample(length(xpoints),1)
      init = c(((init[1] + xpoints[n])*dis), ((init[2] + ypoints[n])*dis))
      if(i<20){
        c='red'
      }else{
        c='blue'
      }
      points(init[1], init[2], cex = 0.5, col=c)
    }
  }
  plot(0:4, 0:4, type = "n")
  e1(xpoints=c(0,3,4), ypoints=c(0,4,1), init=c(1,3), dis=1/2)
  plot(0:4, 0:4, type = "n")
  e1(xpoints=c(0,2,4), ypoints=c(0,2*sqrt(3),0), init=c(1,3), dis=1/2)
  plot(0:4, 0:4, type = "n")
  e1(xpoints=c(0,4,8,8,8,4,0,0), ypoints=c(0,0,0,4,8,8,8,4), init=c(1,3), dis=1/3)
  plot(0:4, 0:4, type = "n")
  e1(xpoints=c(1.4,0.3,3,5.7,4.6), ypoints=c(0,4.7,8,4.7,0), init=c(1,3), dis=1/3)
  plot(0:4, 0:4, type = "n")
  e1(xpoints=c(0,4,8,4,2,4,6,4), ypoints=c(4,8,4,0,4,6,4,2), init=c(1,3), dis=1/3)
  plot(0:4, 0:4, type = "n")
  e1(xpoints=c(0,8,8,0,3.4,3.4,4.6,4.6), ypoints=c(0,0,8,8,4.6,3.4,3.4,4.6), init=c(1,3), dis=1/3)
  return("the smaller the threshole, the longer it takes to run.")
}

# Challenge question G should be written in a separate file that has no dependencies on any functions here.


