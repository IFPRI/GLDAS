
library(foreign)
setwd("D:/Users/cmarciniak/tables")


files <- list.files(pattern = "\\.dbf$")


change.files <- function(file){
  data <- read.dbf(file)
  data$avg_surf_temp <- data$MEAN-272.15
  write.table(data, quote=FALSE, sep=", ", sub("\\.csv$","-edit.txt", file))
}


lapply(change.files,files)
