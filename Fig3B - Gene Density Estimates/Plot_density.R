library(tidyverse)
library(gridExtra)
library(ggsignif)
library(ggpubr)

clean_set <- function(set){
    
    set %<>% filter(Prime3 != "None") %>% filter(Prime5 != "None")
    
    set$Prime5log <- log10(as.numeric(set$Prime5))
    set$Prime3log <- log10(as.numeric(set$Prime3))
    
    return(set)
}

name_col <- function(set, name){
    name_vec <- rep(name, nrow(set))
    
    return(cbind(set,name_vec))
}



setwd("/mnt/nemahomes/steen176/genome_comparisons/distances_figure/")
total_set <- read.csv("total_set_distances.tsv", sep ='\t', stringsAsFactors = F) 
total_set %<>% clean_set %>% name_col(name = 'Total') %>% 
    cbind(., as.numeric(apply(.,1, FUN = function(r){return(min(as.numeric(r['Prime3']),as.numeric(r['Prime5'])))})))
    
CWDE_set <- read.csv("cwde_set_distances.tsv", sep = '\t', stringsAsFactors = F)
CWDE_set %<>% clean_set %>% name_col(name = 'SG') %>% 
    cbind(., as.numeric(apply(.,1, FUN = function(r){return(min(as.numeric(r['Prime3']),as.numeric(r['Prime5'])))})))

GH30_set <- read.csv("GH30_19_set.tsv", sep = '\t', stringsAsFactors = F)
GH30_set %<>% clean_set %>% name_col(name = 'GH30') %>% 
    cbind(., as.numeric(apply(.,1, FUN = function(r){return(min(as.numeric(r['Prime3']),as.numeric(r['Prime5'])))})))

GH5_set <- read.csv("GH5_set_distances.tsv", sep = '\t', stringsAsFactors = F)
GH5_set %<>% clean_set %>% name_col(name = 'GH5') %>% 
    cbind(., as.numeric(apply(.,1, FUN = function(r){return(min(as.numeric(r['Prime3']),as.numeric(r['Prime5'])))})))


sprysec_set <- read.csv("sprysec_set_distances.tsv", sep = '\t', stringsAsFactors = F)    
sprysec_set %<>% clean_set  %>% 
cbind(., as.numeric(apply(.,1, FUN = function(r){return(min(as.numeric(r['Prime3']),as.numeric(r['Prime5'])))})))

HYP_set <- read.csv("HYP_set_distances.tsv", sep = '\t', stringsAsFactors = F)    
HYP_set %<>% clean_set %>% 
    cbind(., as.numeric(apply(.,1, FUN = function(r){return(min(as.numeric(r['Prime3']),as.numeric(r['Prime5'])))})))

Immune_set <- rbind(sprysec_set, HYP_set) %>% name_col("DG")

busco_set <- read.csv("busco_set_distances.tsv", sep = '\t', stringsAsFactors = F)    
busco_set %<>% clean_set %>% name_col(name = 'BUSCO') %>% 
    cbind(., as.numeric(apply(.,1, FUN = function(r){return(min(as.numeric(r['Prime3']),as.numeric(r['Prime5'])))})))


FSF_set <- read.csv("Feeding_site_set_distances.tsv", sep = '\t', stringsAsFactors = F)
FSF_set %<>% clean_set %>% name_col(name = "DG") %>% 
    cbind(., as.numeric(apply(.,1, FUN = function(r){return(min(as.numeric(r['Prime3']),as.numeric(r['Prime5'])))})))


SG_set <- rbind(CWDE_set)
DG_set <- rbind(FSF_set, Immune_set)

combined_table <- rbind(total_set, busco_set, SG_set, DG_set )
colnames(combined_table) <- c("GeneName", "Prime3", "Prime5","Prime5log","Prime3log", "name_vec", 'shortest')



combined_table$name_vec %<>% factor(levels = c('Total', 'BUSCO',"SG","DG"), ordered = TRUE)
combined_table$shortestLog <- log10(combined_table$shortest)







combinations_busco_all <- list(c('Total', 'BUSCO'),c('BUSCO','SG'), c('BUSCO','DG'))
combinations_total_all <- list(c('total', 'BUSCO'),c('total','CWDE'), c('total','Feedingsite'), c('Immune','total'))




ggplot(data = combined_table, aes(x=name_vec, y = shortestLog, fill = name_vec)) +
    geom_violin() +
    stat_compare_means(comparisons = combinations_busco_all, method = 'wilcox.test', label = 'p.signif') + 
    ggtitle("Shortest distance") + labs(y = "Log10 Shortest Distance", x = '') + theme_minimal() 







