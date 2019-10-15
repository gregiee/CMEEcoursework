

a <- NA
for (i in 1:10) {
    a <- c(a, i)
    print(a)
    print(object.size(a))
}



a <- rep(NA, 10)

for (i in 1:10) {
    a[i] <- i
    print(a)
    print(object.size(a))
}

