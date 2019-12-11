library(dplyr)
library(ggplot2)
MyData <- read.csv("Data/LogisticGrowthData.csv")
Species = unique(MyData$Species)
# for(s in Species) {
#   sData = filter(MyData,  Species == s)
#   Medium = unique(sData$Medium)
#   for(m in Medium){
#     mData = filter(sData, Medium == m)
#     Temp =  unique(mData$Temp)
#     pdf(paste0("Results/",s,"-",m,".pdf"))
#     par(mfrow=c(3,2))
#     for(t in Temp) {
#       tData = filter(mData, Temp == t)
#       plot(tData$Time, tData$PopBio, log = "y", main = paste(s,m,t,sep = "\n"))
#       print(paste0("Species: ",s,", Medium: ", m,", temp: ",t))
#       print(nrow(tData))
#     }
#     dev.off()
#   }
# }
pdf("Results/test.pdf") 
for(s in Species) {
  sData = filter(MyData,  Species == s)
  p <- 
    ggplot(sData, aes(x = Time, y = PopBio,color = Medium)) + 
    geom_point(shape = 2) +
    facet_grid(rows = vars(Temp)) +
    scale_y_log10()+
    xlab("time") + 
    ylab("pop(log)") +
    theme_bw()
  print(p)
  }
dev.off()