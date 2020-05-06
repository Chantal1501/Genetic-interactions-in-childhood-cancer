# ==============================================
# Function to plot the mutation rate in CBTTC
# ==============================================

plotMutRate<-function(mutrates, dfcols, rotate){
  tab.freq <- data.frame(table(mutrates$ct))
  colnames(tab.freq) <- c("ct", "frequency")
  tab.freq$ct<-as.character(tab.freq$ct)
  tab.median<-tapply(mutrates$mutcount,mutrates$ct,FUN=median)
  m<-match(tab.freq$ct,names(tab.median))
  tab.freq$median.mutrate<-tab.median[m]
  levels<-tab.freq$ct[order(tab.freq$median.mutrate, decreasing=T)] 
  cols<-dfcols$col[match(mutrates$ct,dfcols$ct)]
  options(scipen=999)
  plot.mutrate<-ggplot(mutrates, 
                       aes(x = factor(ct,levels=levels), 
                           y = mutcount, colour = cols)) + 
    geom_point(shape = 19, position = position_jitter(width = 0.3, height = 0.01)) + 
    geom_boxplot(outlier.shape = NA, alpha = 0.5, show.legend = FALSE) +
    scale_colour_identity() +
    theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5,
                                     size = 8, color="black"), 
          axis.text.y = element_text(color="black", size=8),
          panel.background = element_rect(fill = "transparent"),
          panel.border = element_rect(colour = "black", fill = NA, size = 0.3),
          legend.background = element_rect(colour = NA),
          plot.margin = margin(t=1, r=0.25, b=ifelse(rotate,0.25,1), l=1, "cm")) +
    geom_hline(yintercept = 224, colour = "gray") +
    scale_y_continuous(trans = 'log10', breaks = c(1,2, 6, 51, 501, 5001, 50001, 500001),
                       labels = c(0,1, 5, 50, 500, 5000, 50000, 500000))+
    xlab("") + ylab("number of coding mutations")
}


# =======================================================================================
# Function to plot the mutation rate of the overlapping cancer types in CBTTC and DKFZ
# =======================================================================================

plotMutRate_datasets<-function(mutrates, dfcols, rotate){
  tab.freq <- data.frame(table(mutrates$ct))
  colnames(tab.freq) <- c("ct", "frequency")
  tab.freq$ct<-as.character(tab.freq$ct)
  tab.median<-tapply(mutrates$mutcount,mutrates$ct,FUN=median)
  m<-match(tab.freq$ct,names(tab.median))
  tab.freq$median.mutrate<-tab.median[m]
  levels<-tab.freq$ct#[order(tab.freq$median.mutrate, decreasing=T)] 
  cols<-dfcols$col[match(mutrates$ct,dfcols$ct)]
  options(scipen=999)
  plot.mutrate<-ggplot(mutrates, 
                       aes(x = factor(ct,levels=levels), 
                           y = mutcount, colour = cols)) + 
    geom_point(shape = 19, position = position_jitter(width = 0.3, height = 0.01)) + 
    geom_boxplot(outlier.shape = NA, alpha = 0.5, show.legend = FALSE) +
    scale_colour_identity() +
    theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5,
                                     size = 8, color="black"), 
          axis.text.y = element_text(color="black", size=8),
          panel.background = element_rect(fill = "transparent"),
          panel.border = element_rect(colour = "black", fill = NA, size = 0.3),
          legend.background = element_rect(colour = NA),
          plot.margin = margin(t=1, r=0.25, b=ifelse(rotate,0.25,1), l=1, "cm")) +
    geom_hline(yintercept = 224, colour = "gray") +
    scale_y_continuous(trans = 'log10', breaks = c(1,2, 6, 51, 501, 5001, 50001, 500001),
                       labels = c(0,1, 5, 50, 500, 5000, 50000, 500000))+
    xlab("") + ylab("number of coding mutations")
}



# ===================================================
# Plot number of mutated genes per sample in CBTTC
# ===================================================
library(ggplot2)
dir.analysis <- "D:/Chantal/Data"
par(mfrow=c(1,1))
ct.tab <- read.table(file.path(dir.analysis, "only_all_CTs_CBTTC.txt"), header=F, sep="\t",
                     stringsAsFactors = F, quote = '"', comment.char = "")
ct.tab <- ct.tab[order(ct.tab$ct),]
colnames(ct.tab)<- c("ct", "color", "CTlong", "CTname")
ct.mutrates <- read.table(file.path(dir.analysis, "mutation_rates_silent.txt"), header=T, sep="\t",
                          stringsAsFactors = F, quote = '"', comment.char = "")

plot.mutrate.cbttc<-plotMutRate(mutrates=ct.mutrates, dfcols=ct.tab, rotate=F)
plot.mutrate.cbttc


# =====================================================================================
# Plot number of mutated genes per sample in overlapping cancer types CBTTC and DKFZ
# =====================================================================================
library(ggplot2)
dir.analysis <- "D:/Chantal/Data"
par(mfrow=c(1,1))
ct.tab <- read.table(file.path(dir.analysis, "CTs_overlapping.txt"), header=F, sep="\t",
                     stringsAsFactors = F, quote = '"', comment.char = "")
ct.tab <- ct.tab[order(ct.tab$ct),]
colnames(ct.tab)<- c("ct", "color", "CTlong", "CTname")
ct.mutrates <- read.table(file.path(dir.analysis, "mutation_rates_overlapping.txt"), header=T, sep="\t",
                          stringsAsFactors = F, quote = '"', comment.char = "")
ct.mutrates$mutcount <- ct.mutrates$mutcount + 1
plot.mutrate.cbttc<-plotMutRate_datasets(mutrates=ct.mutrates, dfcols=ct.tab, rotate=F)
plot.mutrate.cbttc


# ==================================================================
# Plot number of mutations per dataset, excluding silent mutations.
# ==================================================================
dir.analysis <- "D:/Chantal/Data"
ct.tab <- read.table(file.path(dir.analysis, "mutation_rate_datasets.txt"))
colnames(ct.tab)<- c("dataset", "sample", "count", "ctype")
boxplot(count~dataset, data=ct.tab, xlab="Dataset", ylab="Number of mutations")

# ============================================================
# What is the mean number of mutations in the three datasets?
# ============================================================
aggregate(ct.tab$count, list(ct.tab$dataset), mean)




