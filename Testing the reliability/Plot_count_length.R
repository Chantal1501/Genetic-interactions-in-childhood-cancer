library("car")
dir.analysis <- "D:/Chantal/Data"
ct.gene_length <- read.table(file.path(dir.analysis, "gene_counts_length.txt"), header = T)

#Scatterplot with on the x-axis count and on the y-axis length
scatterplot(Length ~ Count, data = ct.gene_length)
options(scipen = 999)

#Scatterplot with log scale and on the x-axis length and on the y-axis count
scatterplot(Count ~ Length, data = ct.gene_length, log = "xy")
options(scipen = 999)
