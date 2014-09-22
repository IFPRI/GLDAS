
library(foreign)

setwd("/Path/to/files")

files <- list.files(pattern = "\\.dbf$")

for( i in 1:length(files) ) {
	print( substr( files[i],1,13 ) )
	outfile <- paste( substr(files[i],1,13) ,".csv" ,sep="")
	data <- read.dbf(files[i])
	data$avg_surf_temp = data$MEAN - 272.15
	write.csv(data,outfile,row.names=FALSE)
	
}