# CMEE 2019 HPC excercises R code challenge G proforma

rm(list=ls()) # nothing written elsewhere should be needed to make this work

name <- "Yuchen Yang"
preferred_name <- "Yuchen"
email <- "yuchen.yang19@imperial.ac.uk"
username <- "yy5819"


while (!is.null(dev.list()))  dev.off()
plot(c(0,8),c(0,8),'n')

# don't worry about comments for this challenge - the number of characters used will be counted starting from here
f=function(s,d,l,r){a=c(s[1]+l*cos(d),s[2]+l*sin(d));segments(s[1],s[2],a[1],a[2]);if(l>.01){f(a,d+r*pi/4,l*.38,r);f(a,d,l*.87,-r)}}
f(c(5,0),pi/2,1,1)