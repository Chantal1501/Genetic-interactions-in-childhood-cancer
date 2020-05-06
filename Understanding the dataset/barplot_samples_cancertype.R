#Barplot of the original counts per sample

#Load in the file only_all_CTs_CBTTC.txt. In this file are the colors of the bars present.
dir.analysis <- "D:/Chantal/Data"
ct.tab_cbttc <- read.table(file.path(dir.analysis, "only_all_CTs_CBTTC.txt"), header=F, sep="\t", 
                           stringsAsFactors = F, quote = '"', comment.char = "")
colnames(ct.tab_cbttc)<- c("ct", "color", "CTlong", "CTname")

#Load in the file cancertype_counts.txt. In this file are the counts per cancertype present.  
cbttc.samples <- read.table(file.path(dir.analysis, "cancertype_counts.txt"), header = F, sep = "\t")
colnames(cbttc.samples)<- c("cancertype", "original_count", "final_count")    

#Add the column color and CTlong to the dataframe cbttc.sample.
cbttc.samples$colors <- ct.tab_cbttc$color
cbttc.samples$CTlong <- ct.tab_cbttc$CTlong

#Sort the dataframe on the original count.
cbttc.samples <- cbttc.samples[order(cbttc.samples$original_count),]

#Make it possible that the cancer type name fits correctly.
par(mar=c(5,7,2,4))

#Make the actual barplot, sorted on amount of counts per cancer type.
barplot((cbttc.samples$original_count), names.arg = (cbttc.samples$cancertype), las=2, cex.names = 0.75,
        horiz = TRUE, col = cbttc.samples$colors, xlab = "Amount of samples per cancer type" )

#Add the label cancer types to the y-axis.
mtext(text = "Cancer Types", side = 2, line = 5)

#Plot the legend to the right of the figure.
legend("right", legend =(ct.tab_cbttc$CTlong), pch=15, pt.cex=1, cex=0.5, bty='o',
       col = (ct.tab_cbttc$color))

###################################################################################################

#Stacked bar plot of the original counts and the final counts

#Sort the dataframe on the final count.
stacked_cbttc.samples <- cbttc.samples[order(cbttc.samples$final_count),]

#Put the final count and the difference between the final and the original count together in a dataframe
stacked_cbttc <- rbind(stacked_cbttc.samples$final_count, (stacked_cbttc.samples$original_count - stacked_cbttc.samples$final_count))

#Make it possible that the cancer type name fits correctly.
par(mar=c(5,7,2,4))

#Make the actual stacked barplot, sorted on the final amount of counts per cancer type.
barplot(stacked_cbttc, stack = T, legend = TRUE, col = c("Green", "Red"), names.arg = stacked_cbttc.samples$cancertype, 
        cex.names = 0.75, horiz = TRUE, las = 2, xlab = "Amount of samples per cancer type")

#Add the label cancer types to the y-axis.
mtext(text = "Cancer Types", side = 2, line = 5)

#Plot 2 legends to the right of the figure.
legend(x="bottomright", legend=c("Final count", "Original count"), fill=c("Green", "Red"), cex = 0.6)
legend("right", legend =(ct.tab_cbttc$CTlong), pt.cex=1, cex=0.5, bty='o')#,col = (ct.tab_cbttc$color))

###################################################################################################

#Barplot of the final counts per sample

#Filter the dataset in a way that it only contains the cancer types that are present in the final dataset
filtered_cbttc.samples <- stacked_cbttc.samples[stacked_cbttc.samples$final_count > 0,]

#Make it possible that the cancer type name fits correctly.
par(mar=c(5,8,2,4))

#Make the actual barplot, sorted on amount of counts per cancer type.
barplot((filtered_cbttc.samples$final_count), names.arg = (filtered_cbttc.samples$cancertype), las=2, horiz = TRUE, 
        cex.names = 0.75, col = filtered_cbttc.samples$colors, xlab = "Amount of samples per cancer type", xlim = c(0,250))

#Add the label cancer types to the y-axis.
mtext(text = "Cancer Types", side = 2, line = 6)

#Plot the legend to the right of the figure.
legend("right", legend =(filtered_cbttc.samples$CTlong), pch=15, pt.cex=1, cex=0.5, bty='o',
       col = (filtered_cbttc.samples$color))