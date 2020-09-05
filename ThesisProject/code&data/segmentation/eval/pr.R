setwd("~/Desktop/eval")
# Load the package required to read JSON files.
library("rjson")
# Give the input file name to the function.
result <- fromJSON(file = "ite3/result.json")
resultdf  <- as.data.frame(matrix(unlist(result,FALSE),nrow=6000,ncol=5,byrow = TRUE))
resultdf1 <- as.data.frame(matrix(unlist(resultdf$V5,FALSE),nrow=6000,ncol=2,byrow = TRUE))
resultdf2 <- cbind(resultdf,resultdf1)
predictdf <- resultdf2[,!(names(resultdf2) %in% c("V5"))]
colnames(predictdf) <- c("image_id", "category_id","bbox","score","size","counts")
predictdf <- apply(predictdf,2,as.character)

gt<- fromJSON(file = "ite3/val.json")
gtimage<-as.data.frame(matrix(unlist(gt$images),nrow=60,ncol=5,byrow = TRUE))
colnames(gtimage) <- c("license", "file_name","width","height","image_id")

gtanno <- as.data.frame(matrix(unlist(gt$annotations,FALSE),nrow=400,ncol=7,byrow = TRUE))
colnames(gtanno) <- c("seg", "is_crowd","image_id", "category_id","id","bbox","area")
gtanno <- apply(gtanno,2,as.character)

write.csv(predictdf,"ite3/predictdf.csv")
write.csv(gtimage,"ite3/gtimage.csv")
write.csv(gtanno,"ite3/gtanno.csv")

p <- read.csv(file = 'ite3/predictdf.csv')
gti <- read.csv(file = 'ite3/gtimage.csv')
gta <- read.csv(file = 'ite3/gtanno.csv')

gt <- merge(x = gta, y = gti, by = "image_id", all.x = TRUE)
gt <- gt[,!(names(gt) %in% c("X.x","X.y"))]
write.csv(gt,"ite3/gt.csv")
