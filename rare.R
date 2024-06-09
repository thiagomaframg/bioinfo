#!/usr/bin/env Rscript

library(vegan)

args = commandArgs(trailingOnly=TRUE)

d<-read.csv2(args,sep="\t",row.names=1)
dt<-t(d)
raremax <- min(rowSums(dt))

pdf("Rarefaction_Curve.pdf")
rarecurve(dt, step = 20, sample = raremax, col = "blue", cex = 0.6)
title("Rarefaction Curve")
dev.off()

shannon_2<-diversity(dt,index="shannon",base=2)
write.table(shannon_2,file="Alpha_Diversity_Shannon2.tsv",sep="\t")
