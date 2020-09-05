library(readr)
library(dplyr)

setwd("~/Desktop/t031clustercontour")
contours<- read_csv("resampled_scaled_smoothed_rotated_tulips_220820.csv")
clusters<- read_csv("final.csv")

c1 <- clusters[clusters$`scon$assignments`==1,]
coutours1 <- contours[contours$object_id %in% c1$seg_name,]
c2 <- clusters[clusters$`scon$assignments`==2,]
coutours2 <- contours[contours$object_id %in% c2$seg_name,]
c3 <- clusters[clusters$`scon$assignments`==3,]
coutours3 <- contours[contours$object_id %in% c3$seg_name,]
c4 <- clusters[clusters$`scon$assignments`==4,]
coutours4 <- contours[contours$object_id %in% c4$seg_name,]

write.csv(coutours1,'contourc1.csv')
write.csv(coutours2,'contourc2.csv')
write.csv(coutours3,'contourc3.csv')
write.csv(coutours4,'contourc4.csv')