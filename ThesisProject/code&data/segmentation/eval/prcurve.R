setwd("~/Desktop/eval")
library(tidyverse)
library(data.table)
library(ggplot2)

rawprdf <- read_csv("ite2/PRcal.csv") %>% filter(category_id == 2)
rawprdf <- rawprdf %>% mutate(ioubool = case_when(
  iou>=0.5 ~ 1,
  iou<0.5 ~ 0
))
rawprdf <- rawprdf %>%
  group_by(gt) %>%
  arrange(desc(score)) %>%
  mutate(tpfp1 = case_when(
    ioubool==1 ~ "T",
    ioubool==0 ~ "F",
  )) %>%
  mutate(tpfp = replace(tpfp1, duplicated(tpfp1), "F")) %>%
  ungroup()
rawprdf <- rawprdf[order(rawprdf$tpfp),]
rawprdf <- transform(rawprdf, tfcounter = ave(tpfp, rleid(tpfp), FUN = seq_along))
rawprdf <- rawprdf[order(rawprdf$score, decreasing = TRUE),]
rawprdf$tfcounter <- as.numeric(as.character(rawprdf$tfcounter))
rawprdf <- rawprdf %>% mutate(tcounter = ifelse(tpfp=="F", NA, tfcounter))
rawprdf$tcounter <- as.numeric(as.character(rawprdf$tcounter))
rawprdf$tcounter <- nafill(rawprdf$tcounter, type = "locf")
rawprdf <- rawprdf %>% mutate(recall = tcounter/41)
rawprdf <- rawprdf %>% mutate(precision = tcounter/row_number())
# 1-saz
# 2-carnation
# 3-tulip
rawprdf <- rawprdf[,!(names(rawprdf) %in% c("X1","tpfp1","gtcount"))]
write.csv(rawprdf,"ite2/rawprdf_carnation.csv")

rawprdf1 <- read_csv("ite1/rawprdf_carnation.csv")
rawprdf2 <- read_csv("ite2/rawprdf_carnation.csv")
rawprdf3 <- read_csv("ite3/rawprdf_carnation.csv")

rawprdf1 <- read_csv("ite1/rawprdf.csv")
rawprdf2 <- read_csv("ite2/rawprdf.csv")
rawprdf3 <- read_csv("ite3/rawprdf.csv")

ggplot() +
  geom_line(data=rawprdf1[,c("recall","precision")], aes(x=recall, y=precision, linetype = "repetition1"))+
  geom_line(data=rawprdf2[,c("recall","precision")], aes(x=recall, y=precision, linetype = "repetition2") )+
  geom_line(data=rawprdf3[,c("recall","precision")], aes(x=recall, y=precision, linetype = "repetition3"))+
  scale_linetype_manual(name="",labels = c("Repetition1", "Repetition2","Repetition3"), values=c("twodash", "solid", "dotted"))+
  xlab("Recall") + 
  ylab("Precision")+
  theme_classic()+ 
  theme(legend.position="bottom",
        axis.title=element_text(size=14))

ar5 <- c(0.795, 0.761,0.812)
mean(ar5)
sd(ar5)
  

rawprdf <- read_csv("ite2/PRcal.csv") %>% filter(category_id == 2)
  