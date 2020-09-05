library(readr)
library(dplyr)
library(filesstrings)
setwd("~/Desktop/t04segmentation/seg/iznik")
m<- read_csv("motif_props_all_10-06-20_with_bg_0107.csv")
q<-unique(m$name)
length(unique(m$name))
vc<-sample(q, 60)
val <- m[m$name %in% vc,]
train <- m[!m$name %in% vc,]
write.csv(val,"ite2/val_list.csv")
write.csv(train,"ite2/train_list.csv")
v <- read_csv("ite2/val_list.csv")
t <- read_csv("ite2/train_list.csv")

vl<-unique(v$name)
vc<- v[!grepl("_a", v$seg_name),]
vc<-vc[!(vc$seg_name %in% c("MET43_2_0001_s","LACMA05_1_0008_t","VA01_1_0001_s",
                            "VA30_3_0007_s","VA07_1_0005_s","KOC03_3_0002_c","IPOT04_1_0001_c",
                            "TLCM16_3_0002_t", "TLCM15_1_0000_c")),]

vcl<-unique(vc$seg_name)

tl<-unique(t$name)
tc<- t[!grepl("_a", t$seg_name),]
tc<-tc[!(tc$seg_name %in% c("MET43_2_0001_s","LACMA05_1_0008_t","VA01_1_0001_s",
                            "VA30_3_0007_s","VA07_1_0005_s","KOC03_3_0002_c","IPOT04_1_0001_c",
                            "TLCM16_3_0002_t", "TLCM15_1_0000_c")),]
tcl<-unique(tc$seg_name)
vlist<- paste0("~/Desktop/t04segmentation/seg/iznik/merged/" ,vl, ".jpg")
tlist<- paste0("~/Desktop/t04segmentation/seg/iznik/merged/" ,tl, ".jpg")
vclist<- paste0("~/Desktop/t04segmentation/seg/iznik/contour_csvs/" ,vcl, ".csv")
tclist<- paste0("~/Desktop/t04segmentation/seg/iznik/contour_csvs/" ,tcl, ".csv")
filestocopyv <- c(vlist)
filestocopyt <- c(tlist)
filestocopyvc <- c(vclist)
filestocopytc <- c(tclist)
# identify the folders
new.folderv <- "~/Desktop/t04segmentation/seg/iznik/ite2/val/images"
new.foldert <- "~/Desktop/t04segmentation/seg/iznik/ite2/train/images"
new.foldervc <- "~/Desktop/t04segmentation/seg/iznik/ite2/val/ct"
new.foldertc <- "~/Desktop/t04segmentation/seg/iznik/ite2/train/ct"
# copy the files to the new folder
# setwd("~/Desktop/seg/iznik/merged")
file.copy(filestocopyv, new.folderv, overwrite = TRUE)
file.copy(filestocopyt, new.foldert, overwrite = TRUE)
file.copy(filestocopyvc, new.foldervc, overwrite = TRUE)
file.copy(filestocopytc, new.foldertc, overwrite = TRUE)
  
