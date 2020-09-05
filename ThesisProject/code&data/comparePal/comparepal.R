setwd("~/Desktop/t02comparepal")
library(readr)
library(dplyr)
library(tidyverse)
library(scatterplot3d)

discover10<-read_csv("data/palette_10_unconstrained_090720.csv")
image(1:nrow(discover10), 1, as.matrix(1:nrow(discover10)),
      col=rgb(discover10$R, discover10$G, discover10$B, maxColorValue = 255),
      xlab="", ylab = "", xaxt = "n", yaxt = "n", bty = "n")

expertraw<-read_csv("data/canonical_colour.csv")
expertrawwona<-expertraw%>%drop_na("r")
expertmean<-expertrawwona%>%
  group_by(colour_id)%>%
  summarise(R=mean(r),G=mean(g),B=mean(b))
image(1:nrow(expertmean), 1, as.matrix(1:nrow(expertmean)),
      col=rgb(expertmean$R, expertmean$G, expertmean$B, maxColorValue = 255),
      xlab="", ylab = "", xaxt = "n", yaxt = "n", bty = "n")

discover10$shape <- 15
discover10[, c("L","A","B1")] <- convertColor(discover10[, c("R","G","B")], from = "sRGB", to = "Lab", scale.in = 255, scale.out = 1)
expertmean$shape <- 17
expertmean[, c("L","A","B1")] <- convertColor(expertmean[, c("R","G","B")], from = "sRGB", to = "Lab", scale.in = 255, scale.out = 1)

colourd<- apply(discover10[,  c("R","G","B")], 1, function (x) rgb(x[1], x[2], x[3], 255, maxColorValue=255))
coloure<- apply(expertmean[,  c("R","G","B")], 1, function (x) rgb(x[1], x[2], x[3], 205, maxColorValue=255))
colourall<-c(colourd,coloure)

allcolours<- rbind(discover10[,c("L","A","B1","shape")],expertmean[,c("L","A","B1","shape")])

fig3d<-scatterplot3d(allcolours[, c("A", "B1","L")], 
                     pch = allcolours$shape, 
                     color= colourall,
                     box=FALSE,
                     xlab="A(green to red)", 
                     ylab="B(blue to yellow)", 
                     zlab="L(lightness)",
                     cex.lab=.9,
                     cex.symbols=2,
                     type="h"
                     )
legend("bottom", legend = c("Discover", "Expert"),
       pch = c(15,17),
       inset = 0, xpd = TRUE, horiz = TRUE)




par(mfrow=c(3,4))
par(mar=c(1,1,1,1))
seq <-  unique(expertrawwona$colour_id)
for (colour in seq)
{
  df<-expertrawwona[expertrawwona$colour_id==colour,]
  image(1:nrow(df), 1, as.matrix(1:nrow(df)),
        col=rgb(df$r, df$g, df$b, maxColorValue = 255),
        xlab="", ylab = "", xaxt = "n", yaxt = "n", bty = "n",main=colour,)
}
