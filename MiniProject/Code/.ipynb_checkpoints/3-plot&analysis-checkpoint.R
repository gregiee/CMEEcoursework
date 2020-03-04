# Author: Yuchen Yang (yy5819@ic.ac.uk)
# Version: 0.0.1
## Clear the directory ##
rm(list=ls())

# import the results from the previous step and plot every curve with the models (or none, if nothing converges) overlaid. 
# Doing this will help you identify poor fits visually and help you decide whether the previous.
# NLLS fitting script can be further optimized (e.g., by improving the starting values generator). 
# All plots should be saved in a single separate sub-directory. 

# load requirements and data
require(ggplot2)
graphData <- read.csv("../Data/graphdf.csv", stringsAsFactors=FALSE)
analysisData <- read.csv("../Data/analysisdf.csv", stringsAsFactors=FALSE)

IDlen <- length(analysisData$ID)-1
# draw all fitting results
for (i  in  0:IDlen){
  print(i)
  #!!!!!change the size of the canvas
  name = paste(analysisData[analysisData$ID==i, 1],
              analysisData[analysisData$ID==i, 2],
              analysisData[analysisData$ID==i, 3],
              analysisData[analysisData$ID==i, 4],
              sep = "_")
  subt = paste("Temp: ", analysisData[analysisData$ID==i, 2],
               "Medium: ", analysisData[analysisData$ID==i, 3],
               "Species: ", analysisData[analysisData$ID==i, 4],
               sep = "\n")
  drawdf = subset(graphData, ID==i)
  color = c("logistic"="#2F4073", "gompertz"="#048C7F", 
            "baranyi"="#F2AC29","poly"="#BF4141")
  ggplot(drawdf, aes(x)) + 
    geom_point(aes(y = logisticFit, colour = "logistic"), shape = 3, size = .7, stroke = .7, alpha = 1) + 
    geom_point(aes(y = gompertzFit, colour = "gompertz"), shape = 3, size = .7, stroke = .7, alpha = 1) + 
    geom_point(aes(y = baranyiFit, colour = "baranyi"),  shape = 3, size = .7, stroke = .7, alpha = 1) + 
    geom_point(aes(y = polyFit, colour = "poly"),  shape = 3, size = .7, stroke = .7, alpha = 1) + 
    geom_line(aes(y = logisticFit, colour = "logistic"),linetype = "solid", size = .4)+ 
    geom_line(aes(y = gompertzFit, colour = "gompertz"),linetype = "solid", size = .4)+ 
    geom_line(aes(y = baranyiFit, colour = "baranyi"),linetype = "solid", size = .4)+ 
    geom_line(aes(y = polyFit, colour = "poly"),linetype = "solid", size = .4)+
    geom_point(aes(y = y), colour = "black", size = 1.5) +
    scale_colour_manual("", 
                        breaks = c("logistic", "gompertz", "baranyi", "poly"),
                        values = color ) +
    labs(title = paste("ID:", i),
         subtitle = subt,
         caption = "", 
         x = "Time", y = "Ln(Pop)")+
    theme(plot.title = element_text(size = 10, colour = "black"),
          plot.subtitle = element_text(size = 8, colour = "grey"),
          axis.title = element_text(size = 8))
    theme_minimal()
  
  filename <- paste("../Results/allPlots/",name,".pdf")
  ggsave(filename)
}

