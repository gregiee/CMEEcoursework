library(readr)
library(dplyr)
library(ggplot2)
library(tidyr)
library(Spectrum)
library(proxy)
library(reshape2)
library(tidyverse)


setwd("~/Desktop/t031clustercontour")

data<- read_csv("resampled_scaled_smoothed_rotated_tulips_220820.csv")

id <- sort(unique(data$object_id), decreasing = FALSE)
a <- data %>% 
  group_by(object_id) %>% 
  arrange(desc(object_id)) %>%
  select(x, y)  %>%
  group_map(~ c(t(.x)))
aa <- data.frame(Reduce(rbind, a))
pcaraw <- cbind(id=id, aa)

coord <- pcaraw[,-1]
rownames(coord) <- pcaraw[,1]

scaled.coord <- scale(coord)

coord.pca <- prcomp(coord)
summary(coord.pca)
plot(coord.pca$x[,1], coord.pca$x[,2])


#==========================
data2<- read_csv("10color_25shape_1ratio_t_new.csv")
plot(data2$Comp.1, data2$Comp.2)


colour <- data2[,c("perc_0","perc_1","perc_2",
                   "perc_3","perc_4","perc_5",
                   "perc_6","perc_7","perc_8",
                   "perc_9")]
col <-  as.data.frame(t(as.matrix(colour)))
shapes <- data2[,c("Comp.1","Comp.2","Comp.3","Comp.4",
                   "Comp.5","Comp.6","Comp.7","Comp.8",
                   "Comp.9","Comp.10","Comp.11","Comp.12",
                   "Comp.13","Comp.14","Comp.15","Comp.16",
                   "Comp.17","Comp.18","Comp.19","Comp.20")]
shape <-  as.data.frame(t(as.matrix(shapes)))
size <- data2[,c("ratio")]
siz <- as.data.frame(t(as.matrix(size$ratio)))
size$Category[size$ratio < 0.01] = 1
size$Category[size$ratio >= 0.01 & size$ratio <= 0.05] = 2
size$Category[size$ratio > 0.05] = 3


ggplot(size) +
  geom_bar(aes(x = as.factor(Category),  fill = as.factor(Category)), width=0.2) +
  scale_color_viridis(discrete = TRUE, option = "D")+
  scale_fill_viridis(discrete = TRUE, option = "D")+
  theme_classic()+
  theme(aspect.ratio = 1)+
  theme(legend.position="bottom")+
  xlab("Category") +
  theme(legend.title = element_blank(),axis.title=element_text(size=10))

data2$sizeCat <- size$Category
# siz <-  as.data.frame(t(as.matrix(size$Category)))
dflist <- list(col, shape)

sall<- Spectrum(dflist, showpca=TRUE, fontsize=8, dotsize=2, method=2, maxk=50)
finalall <- cbind(data2, sall$assignments)
write.csv(finalall,"finalall.csv")

scol<- Spectrum(col, showpca=TRUE, fontsize=8, dotsize=1, method=2, maxk=50)
final <- cbind(data2, scol$assignments)

scon<- Spectrum(shape, showpca=TRUE, fontsize=8, dotsize=1, method=2, maxk=50)
final <- cbind(final, scon$assignments)

# ssiz<- Spectrum(siz, showpca=TRUE, fontsize=8, dotsize=2, method=2, maxk=50)
# final <- cbind(final, ssiz$assignments)
write.csv(final,"final.csv")

# ===================
pal<- read_csv("palette_10_unconstrained_090720.csv")

drawcluster <- function (cluster, df) {
  cluster1 <- df %>% 
    filter(scol$assignments==cluster) %>%
    select(seg_name,
           perc_0,perc_1,perc_2,
           perc_3,perc_4,perc_5,
           perc_6,perc_7,perc_8,
           perc_9)
  cluster1long <- reshape(cluster1, 
                          direction = "long",
                          varying = list(names(cluster1)[2:11]),
                          v.names = "Value")
  ggplot(cluster1long, aes(fill=as.factor(time), y=Value, x=seg_name)) + 
    geom_bar(position="fill", stat="identity") +
    scale_fill_manual(breaks = c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"), 
                      values= c(rgb(pal$R[1], pal$G[1], pal$B[1], maxColorValue = 255),
                                rgb(pal$R[2], pal$G[2], pal$B[2], maxColorValue = 255),
                                rgb(pal$R[3], pal$G[3], pal$B[3], maxColorValue = 255),
                                rgb(pal$R[4], pal$G[4], pal$B[4], maxColorValue = 255),
                                rgb(pal$R[5], pal$G[5], pal$B[5], maxColorValue = 255),
                                rgb(pal$R[6], pal$G[6], pal$B[6], maxColorValue = 255),
                                rgb(pal$R[7], pal$G[7], pal$B[7], maxColorValue = 255),
                                rgb(pal$R[8], pal$G[8], pal$B[8], maxColorValue = 255),
                                rgb(pal$R[9], pal$G[9], pal$B[9], maxColorValue = 255),
                                rgb(pal$R[10], pal$G[10], pal$B[10], maxColorValue = 255))) +
    theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))
  ggsave(paste(cluster,"_all.pdf"), device = "pdf")
}

# for (i in 1:14) {
#   drawcluster(i,finalall)
# }
for (i in 1:10) {
  drawcluster(i,final)
}

# ====================================
pal<- read_csv("palette_10_unconstrained_090720.csv")
finalall<- read_csv("final.csv")
cluster1 <- finalall %>% 
  group_by(`scol$assignments`) %>%
  summarise_all(list(mean))%>%
  select(`scol$assignments`,
         perc_0,perc_1,perc_2,
         perc_3,perc_4,perc_5,
         perc_6,perc_7,perc_8,
         perc_9)

cluster1long <- melt(cluster1,id.vars = "scol$assignments")
ggplot(cluster1long, aes(fill=as.factor(variable), y=value, x=as.factor(`scol$assignments`))) + 
  geom_bar(position="fill", stat="identity") + 
  scale_fill_manual(breaks = c("perc_0", "perc_1", "perc_2", "perc_3", "perc_4", "perc_5",
                               "perc_6", "perc_7", "perc_8", "perc_9"),
                    values= c(rgb(pal$R[1], pal$G[1], pal$B[1], maxColorValue = 255),
                              rgb(pal$R[2], pal$G[2], pal$B[2], maxColorValue = 255),
                              rgb(pal$R[3], pal$G[3], pal$B[3], maxColorValue = 255),
                              rgb(pal$R[4], pal$G[4], pal$B[4], maxColorValue = 255),
                              rgb(pal$R[5], pal$G[5], pal$B[5], maxColorValue = 255),
                              rgb(pal$R[6], pal$G[6], pal$B[6], maxColorValue = 255),
                              rgb(pal$R[7], pal$G[7], pal$B[7], maxColorValue = 255),
                              rgb(pal$R[8], pal$G[8], pal$B[8], maxColorValue = 255),
                              rgb(pal$R[9], pal$G[9], pal$B[9], maxColorValue = 255),
                              rgb(pal$R[10], pal$G[10], pal$B[10], maxColorValue = 255)))




# =========================================

final<- read_csv("final.csv")

colourd <- final[,c("perc_0","perc_1","perc_2",
                    "perc_3","perc_4","perc_5",
                    "perc_6","perc_7","perc_8",
                    "perc_9","scol$assignments")]

coord.pca <- prcomp(colourd[,1:10])
summary(coord.pca)
plot(coord.pca$x[,1], coord.pca$x[,2])
final$c1 <- coord.pca$x[,1]
final$c2 <- coord.pca$x[,2]

library("viridis")    

ggplot()+
  geom_point(data=final , aes(x=c1, y=c2, color=as.factor(`scol$assignments`)), 
             alpha=0.7, size=0.8)+
  scale_color_viridis(discrete = TRUE, option = "D")+
  theme_classic()+
  theme(aspect.ratio = 1)+
  theme(legend.position="bottom")+
  theme(legend.title = element_blank(),axis.title=element_text(size=10))+
  scale_x_continuous(name="shape PC1")+
  scale_y_continuous(name="shape PC2")

# =============================

grammar <- final[,c("ID","sizeCat","scol$assignments","scon$assignments")]
colnames(grammar) <- c("ID", "size", "colour", "shape")
grammar <- grammar %>% 
  mutate(group = paste0(size,colour,shape))%>%
  mutate(artefact = sapply(strsplit(ID, split='_', fixed=TRUE),function(x) (x[1])))

grammarc <- grammar %>%
  group_by(artefact)%>%
  summarise(countunique = n_distinct(group), total.count=n())

summary(grammarc)
length(unique(grammar$group))


# ================================
library(vegan)
data(BCI)
BCI1 <- data.frame(rbind(table(grammar$group)))
#total number of species at each site (row of data)
S <- specnumber(BCI)

# Number of INDIVIDULS per site (?)
raremax <- min(rowSums(BCI)) # = 340; 

# rarefy, w/ raremax as input (?)
Srare <- rarefy(BCI, raremax)

#Plot rarefaction results
# par(mfrow = c(1,2))
plot(S, Srare, xlab = "Observed No. of Species", 
     ylab = "Rarefied No. of Species",
     main = " plot(rarefy(BCI, raremax))")
abline(0, 1)
rarecurve(BCI, step = 20, 
          col = "blue", 
          cex = 0.6,
          main = "rarecurve()")

# ===========================
install.packages("iNEXT")

## install the latest version from github
install.packages('devtools')
library(devtools)
install_github('JohnsonHsieh/iNEXT')
library(iNEXT)

data(spider)
str(spider)

BCI.test.no.zero <- unlist(BCI1)

# i.zero <- which(BCI.test.no.zero == 0)
# BCI.test.no.zero <- BCI.test.no.zero[-i.zero]

out <- iNEXT(BCI.test.no.zero, q=0, datatype="abundance", endpoint=1300)
g <- ggiNEXT(out, type=1, facet.var="site")
g1 <- g +
  theme_classic() + 
  scale_fill_grey(start = 0, end = .4) +
  scale_colour_grey(start = .2, end = .2) +
  theme(axis.line = element_line(colour = "black"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.border = element_blank(),
        panel.background = element_blank(),
        strip.background = element_blank(),
        legend.position="bottom",
        legend.title=element_blank(),
        legend.box = "vertical") 
g1
