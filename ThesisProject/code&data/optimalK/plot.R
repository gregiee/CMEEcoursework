setwd("~/Desktop/t01optimalKforpal/optk/clustering_results/")
library(dplyr)
library(tidyverse)
g <- paste(sprintf("%03d", id), "csv", sep = ".")

g<-list.files(pattern = "*.csv")
df <- bind_rows(lapply(g, read_csv), .id = "source")

dfmean <- df%>%
  group_by(clusters)%>%
  summarize(meansil = mean(silhouette_width),
            meanssq = mean(sums_of_squares),
            silsd = sd(silhouette_width),
            ssqsd = sd(sums_of_squares))

a<-df %>% filter(clusters > 2)


ggplot() + 
  # geom_line(data=df %>% filter(clusters > 2), aes(x=clusters, y=silhouette_width, group=source), colour="black", size=.1, alpha = .2)+
  geom_line(data=dfmean[-(1:2),], aes(x=clusters, y=meansil))+
  geom_ribbon(data=dfmean[-(1:2),], aes(x=clusters, y=meansil, ymin=meansil-silsd, ymax=meansil+silsd), alpha = 0.1)+
  # geom_errorbar(data=dfmean[-(1:2),], aes(x=clusters, y=meansil, ymin=meansil-silsd, ymax=meansil+silsd), width=.2, position=position_dodge(0.1))+
  geom_vline(xintercept = 10, linetype="dashed", color = "red", size=.2)+
  xlab("Cluster(K)") + 
  ylab("Silhouette Score")+
  theme_classic()

ggplot() + 
  # geom_line(data=df %>% filter(clusters > 2), aes(x=clusters, y=silhouette_width, group=source), colour="black", size=.1, alpha = .2)+
  geom_line(data=dfmean[-(1:2),], aes(x=clusters, y=meanssq))+
  geom_ribbon(data=dfmean[-(1:2),], aes(x=clusters, y=meanssq, ymin=meanssq-ssqsd, ymax=meanssq+ssqsd), alpha = 0.5)+
  # geom_errorbar(data=dfmean[-(1:2),], aes(x=clusters, y=meansil, ymin=meansil-silsd, ymax=meansil+silsd), width=.2, position=position_dodge(0.1))+
  geom_rect(aes(xmin=8, xmax=12, ymin=-Inf, ymax=Inf), alpha = 0.1)+
  geom_vline(xintercept = 10, linetype="dashed", color = "red", size=.2)+
  xlab("Cluster(K)") + 
  ylab("WSS")+
  theme_classic()

