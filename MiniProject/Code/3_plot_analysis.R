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
require(reshape2)
# turn off warning
options(warn=-1)

graphData <- read.csv("../Data/graphdf.csv", stringsAsFactors=FALSE)
analysisData <- read.csv("../Data/analysisdf.csv", stringsAsFactors=FALSE)

color = c("logistic"="#2F4073", "gompertz"="#048C7F", 
          "baranyi"="#F2AC29","polynomial"="#BF4141")
IDlen <- length(analysisData$ID)-1

print("plotting, might take a few minutes.")
# draw all fitting results
for(i  in  0:IDlen){
  if (i %% 10 == 0){
    print(paste("plotting ", i, " to ", i+9))
  }
  name = as.character(analysisData[analysisData$ID==i, 1])
  subt = paste("Temp: ", analysisData[analysisData$ID==i, 2],
               "Medium: ", analysisData[analysisData$ID==i, 3],
               "Species: ", analysisData[analysisData$ID==i, 4],
               sep = "\n")
  drawdf = subset(graphData, ID==i)
  ggplot(drawdf, aes(x)) + 
    geom_point(aes(y = logisticFit, colour = "logistic"), shape = 3, size = .7, stroke = .7, alpha = 1) + 
    geom_point(aes(y = gompertzFit, colour = "gompertz"), shape = 3, size = .7, stroke = .7, alpha = 1) + 
    geom_point(aes(y = baranyiFit, colour = "baranyi"),  shape = 3, size = .7, stroke = .7, alpha = 1) + 
    geom_point(aes(y = polyFit, colour = "polynomial"),  shape = 3, size = .7, stroke = .7, alpha = 1) + 
    geom_line(aes(y = logisticFit, colour = "logistic"),linetype = "solid", size = .4)+ 
    geom_line(aes(y = gompertzFit, colour = "gompertz"),linetype = "solid", size = .4)+ 
    geom_line(aes(y = baranyiFit, colour = "baranyi"),linetype = "solid", size = .4)+ 
    geom_line(aes(y = polyFit, colour = "polynomial"),linetype = "solid", size = .4)+
    geom_point(aes(y = y), colour = "black", size = 1.5) +
    scale_colour_manual("", 
                        breaks = c("logistic", "gompertz", "baranyi", "polynomial"),
                        values = color ) +
    labs(title = paste("ID:", i),
         subtitle = subt,
         caption = "", 
         x = "Time", y = "Ln(Pop)")+
    theme(plot.title = element_text(size = 10, colour = "black"),
          plot.subtitle = element_text(size = 8, colour = "grey"),
          axis.title = element_text(size = 8))
    theme_minimal()
  
  filename <- paste("../Results/allPlots/",name,".pdf",sep="")
  ggsave(filename, width = 7, height = 4)
}

# This script will also perform any analyses of the results of the Model fitting.
# for example to summarize which model(s) fit(s) best, and address any biological questions involving co-variates.

# generating r^2 overview
r2snap <- melt(analysisData, id.vars='ID', measure.vars=c('lR2','gR2','pR2',"bR2"))
ggplot(r2snap, aes(variable, value)) + 
  geom_boxplot() +
  geom_hline(yintercept=0.8, linetype="dashed") +
  labs(title = "R-squared overview", x ="Model", y = "R^2")
ggsave("../Results/anaPlots/r2snap.pdf", width = 7, height = 4)

# get rid of data sets with r^2 less than 0.75 for all four models
# some r^2 are NA and the rest models' r^2 is less than 0.75 
analysisDataFinal <- analysisData[!(analysisData$lR2<0.75
                                         & analysisData$gR2<0.75
                                         & analysisData$pR2<0.75
                                         & analysisData$bR2<0.75), ]
analysisDataFinal <- analysisDataFinal[rowSums(is.na(analysisDataFinal)) != ncol(analysisDataFinal), ]


# calculating grades for each model for each data group
# creating minAIC for calculating deltaAIC
analysisDataFinal <- cbind(analysisDataFinal, minAIC = apply(
  analysisDataFinal[, c("bAIC", "lAIC", "gAIC", "pAIC")], 
  1, 
  function(x) ifelse(all(is.na(x)), NA, min(x, na.rm=T))))
# calculationg Baranyi deltaAIC
analysisDataFinal$bdAIC <- (analysisDataFinal$bAIC- analysisDataFinal$minAIC)
# calculationg Gompertz deltaAIC
analysisDataFinal$gdAIC <- (analysisDataFinal$gAIC- analysisDataFinal$minAIC)
# calculationg Logistic deltaAIC
analysisDataFinal$ldAIC <- (analysisDataFinal$lAIC- analysisDataFinal$minAIC)
# calculationg Polynomial deltaAIC
analysisDataFinal$pdAIC <- (analysisDataFinal$pAIC- analysisDataFinal$minAIC)

# assign grade points
analysisDataFinal$bp <- ifelse(analysisDataFinal$bdAIC < 2 & !is.na(analysisDataFinal$bdAIC), 1, 0)
analysisDataFinal$gp <- ifelse(analysisDataFinal$gdAIC < 2 & !is.na(analysisDataFinal$gdAIC), 1, 0)
analysisDataFinal$lp <- ifelse(analysisDataFinal$ldAIC < 2 & !is.na(analysisDataFinal$ldAIC), 1, 0)
analysisDataFinal$pp <- ifelse(analysisDataFinal$pdAIC < 2 & !is.na(analysisDataFinal$pdAIC), 1, 0)

# calculating grades for each model for each data group
# creating minAIC for calculating deltaAIC
analysisDataFinal <- cbind(analysisDataFinal, minBIC = apply(
  analysisDataFinal[, c("bBIC", "lBIC", "gBIC", "pBIC")], 
  1, 
  function(x) ifelse(all(is.na(x)), NA, min(x, na.rm=T))))
# calculationg Baranyi deltaAIC
analysisDataFinal$bdBIC <- (analysisDataFinal$bBIC- analysisDataFinal$minBIC)
# calculationg Gompertz deltaAIC
analysisDataFinal$gdBIC <- (analysisDataFinal$gBIC- analysisDataFinal$minBIC)
# calculationg Logistic deltaAIC
analysisDataFinal$ldBIC <- (analysisDataFinal$lBIC- analysisDataFinal$minBIC)
# calculationg Polynomial deltaAIC
analysisDataFinal$pdBIC <- (analysisDataFinal$pBIC- analysisDataFinal$minBIC)

# assign grade points
analysisDataFinal$bbp <- ifelse(analysisDataFinal$bdBIC < 2 & !is.na(analysisDataFinal$bdBIC), 1, 0)
analysisDataFinal$bgp <- ifelse(analysisDataFinal$gdBIC < 2 & !is.na(analysisDataFinal$gdBIC), 1, 0)
analysisDataFinal$blp <- ifelse(analysisDataFinal$ldBIC < 2 & !is.na(analysisDataFinal$ldBIC), 1, 0)
analysisDataFinal$bpp <- ifelse(analysisDataFinal$pdBIC < 2 & !is.na(analysisDataFinal$pdBIC), 1, 0)

# calculate AIC weight with customized function 
`%+%` <- function(x, y)  mapply(sum, x, y, MoreArgs = list(na.rm = TRUE))
analysisDataFinal$bAICw <- exp(analysisDataFinal$bdAIC*(-1/2)) / (exp(analysisDataFinal$bdAIC*(-1/2)) 
                                                                  %+% exp(analysisDataFinal$gdAIC*(-1/2))
                                                                  %+% exp(analysisDataFinal$ldAIC*(-1/2)) 
                                                                  %+% exp(analysisDataFinal$pdAIC*(-1/2)) )
analysisDataFinal$gAICw <- exp(analysisDataFinal$gdAIC*(-1/2)) / (exp(analysisDataFinal$bdAIC*(-1/2)) 
                                                                  %+% exp(analysisDataFinal$gdAIC*(-1/2))
                                                                  %+% exp(analysisDataFinal$ldAIC*(-1/2)) 
                                                                  %+% exp(analysisDataFinal$pdAIC*(-1/2)) )
analysisDataFinal$lAICw <- exp(analysisDataFinal$ldAIC*(-1/2)) / (exp(analysisDataFinal$bdAIC*(-1/2)) 
                                                                  %+% exp(analysisDataFinal$gdAIC*(-1/2))
                                                                  %+% exp(analysisDataFinal$ldAIC*(-1/2)) 
                                                                  %+% exp(analysisDataFinal$pdAIC*(-1/2)) )
analysisDataFinal$pAICw <- exp(analysisDataFinal$pdAIC*(-1/2)) / (exp(analysisDataFinal$bdAIC*(-1/2)) 
                                                                  %+% exp(analysisDataFinal$gdAIC*(-1/2))
                                                                  %+% exp(analysisDataFinal$ldAIC*(-1/2)) 
                                                                  %+% exp(analysisDataFinal$pdAIC*(-1/2)) )

# calculating final point for all
finalGradeForAll <- colSums(analysisDataFinal[,c("bp", "gp", "lp", "pp")])
finalGradeForAllBic <- colSums(analysisDataFinal[,c("bbp", "bgp", "blp", "bpp")])

# weight AIC graph for temp gourps
tempanalysisdf <- subset(analysisDataFinal, Species=="Tetraselmis tetrahele")
tempanalysisdf <- melt(tempanalysisdf,id.vars='Temp', measure.vars=c("bAICw", "gAICw", "lAICw", "pAICw"))
ggplot(tempanalysisdf, aes(x=factor(Temp), y=value, group=factor(variable))) + 
  geom_point(aes(colour = factor(variable)),size = .9, shape = 3)+
  geom_smooth(aes(colour = factor(variable)),level = 0.3)+
  labs(title = "Model performance differences under AIC weight", 
       x = "Temperature groups", y = "AIC weight value")+ 
  
  scale_colour_manual(values = c("#F2AC29", "#048C7F", "#2F4073", "#BF4141"),
                      breaks = c("bAICw", "gAICw", "lAICw", "pAICw"),
                      labels = c("Baranyi", "Gompertz", "Logistic", "Polynomial"))+
  theme(plot.title = element_text(size = 10, colour = "black"),
        plot.subtitle = element_text(size = 8, colour = "grey"),
        axis.title = element_text(size = 8))+
  theme_minimal()
ggsave("../Results/anaPlots/wAICtemp.pdf", width = 7, height = 4)


# # calculate p-value for overall difference for each model across temp groups
# wAICtempb <- subset(tempanalysisdf, variable=="bAICw")
# kruskal.test(value ~ Temp, data = wAICtempb)
# wAICtempg <- subset(tempanalysisdf, variable=="gAICw")
# kruskal.test(value ~ Temp, data = wAICtempg)
# wAICtempl <- subset(tempanalysisdf, variable=="lAICw")
# kruskal.test(value ~ Temp, data = wAICtempl)
# wAICtempp <- subset(tempanalysisdf, variable=="pAICw")
# kruskal.test(value ~ Temp, data = wAICtempp)

# # calculate pairwise p-value for pairwise difference for each model across
# wAICtempb010 <- subset(wAICtempp, Temp=="5"|Temp=="8")
# wilcox.test(value ~ Temp, data = wAICtempb010)
# wAICtempb010 <- subset(wAICtempp, Temp=="5"|Temp=="16")
# wilcox.test(value ~ Temp, data = wAICtempb010)
# wAICtempb010 <- subset(wAICtempp, Temp=="5"|Temp=="25")
# wilcox.test(value ~ Temp, data = wAICtempb010)
# wAICtempb010 <- subset(wAICtempp, Temp=="5"|Temp=="32")
# wilcox.test(value ~ Temp, data = wAICtempb010)
# wAICtempb010 <- subset(wAICtempp, Temp=="8"|Temp=="16")
# wilcox.test(value ~ Temp, data = wAICtempb010)
# wAICtempb010 <- subset(wAICtempp, Temp=="8"|Temp=="25")
# wilcox.test(value ~ Temp, data = wAICtempb010)
# wAICtempb010 <- subset(wAICtempp, Temp=="8"|Temp=="32")
# wilcox.test(value ~ Temp, data = wAICtempb010)
# wAICtempb010 <- subset(wAICtempp, Temp=="16"|Temp=="25")
# wilcox.test(value ~ Temp, data = wAICtempb010)
# wAICtempb010 <- subset(wAICtempp, Temp=="16"|Temp=="32")
# wilcox.test(value ~ Temp, data = wAICtempb010)
# wAICtempb010 <- subset(wAICtempp, Temp=="25"|Temp=="32")
# wilcox.test(value ~ Temp, data = wAICtempb010)


# weight AIC graph for deathPhase gourps
wAICdeathphase <- melt(analysisDataFinal,id.vars='deathPhase', measure.vars=c("bAICw", "gAICw", "lAICw", "pAICw"))
ggplot(wAICdeathphase, aes(variable, value) ) + 
  geom_boxplot()+
  facet_grid(deathPhase~variable , scales = "free", space = "free", margins = T) + 
  labs(x = "wAIC per model", y = "weight")
ggsave("../Results/anaPlots/wAICdeathphase.pdf", width = 7, height = 6)

# # calculate p-value for pairwise difference for each model across deathPhase groups
# wAICdeathphaseb <- subset(wAICdeathphase, variable=="bAICw")
# wilcox.test(value ~ deathPhase, data = wAICdeathphaseb)
# wAICdeathphaseg <- subset(wAICdeathphase, variable=="gAICw")
# wilcox.test(value ~ deathPhase, data = wAICdeathphaseg)
# wAICdeathphasel <- subset(wAICdeathphase, variable=="lAICw")
# wilcox.test(value ~ deathPhase, data = wAICdeathphasel)
# wAICdeathphasep <- subset(wAICdeathphase, variable=="pAICw")
# wilcox.test(value ~ deathPhase, data = wAICdeathphasep)


# calculating final point for temp groups
finalGradeForT<-data.frame()
tempGroup <- unique(analysisData$Temp)
for (i  in  1:length(tempGroup)){
  t <- subset(analysisDataFinal, Temp==tempGroup[i])
  a <- as.data.frame(t(colSums(t[,c("bp", "gp", "lp", "pp")])))
  a$groupCount <- nrow(t)
  finalGradeForT <- rbind(finalGradeForT, a)
}
finalGradeForT$Temp <- tempGroup
finalGradeForT <- finalGradeForT[order(finalGradeForT$Temp),]
finalGradeForT$bpr <- finalGradeForT$bp/finalGradeForT$groupCount
finalGradeForT$gpr <- finalGradeForT$gp/finalGradeForT$groupCount
finalGradeForT$lpr <- finalGradeForT$lp/finalGradeForT$groupCount
finalGradeForT$ppr <- finalGradeForT$pp/finalGradeForT$groupCount


# calculating final point for deathphase group
finalGradeForD<-data.frame()
deathGroup <- unique(analysisData$deathPhase)
for (i  in  1:length(deathGroup)){
  t <- subset(analysisDataFinal, deathPhase==deathGroup[i])
  a <- as.data.frame(t(colSums(t[,c("bp", "gp", "lp", "pp")])))
  a$groupCount <- nrow(t)
  finalGradeForD <- rbind(finalGradeForD, a)
}
finalGradeForD$deathPhase <- deathGroup
finalGradeForD$bpr <- finalGradeForD$bp/finalGradeForD$groupCount
finalGradeForD$gpr <- finalGradeForD$gp/finalGradeForD$groupCount
finalGradeForD$lpr <- finalGradeForD$lp/finalGradeForD$groupCount
finalGradeForD$ppr <- finalGradeForD$pp/finalGradeForD$groupCount

