

################################
library(tidyverse)
library(magrittr)
library(ggplot2)
library(reshape2)




#####################################
data_GH5_19 <- NULL
data_GH5_19 <- Import_table(data_GH5_19, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/GH5_gr19.tsv',
                                'GH5', "CWDE", "L19")
data_GH5_22 <- NULL
data_GH5_22 <- Import_table(data_GH5_22, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/GH5_gr22.tsv',
                            'GH5', "CWDE", "L22")

data_GH30_19 <- NULL
data_GH30_19 <- Import_table(data_GH30_19, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/GH30_gr19.tsv',
                            'GH30', "CWDE", "L19")
data_GH30_22 <- NULL
data_GH30_22 <- Import_table(data_GH30_22, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/GH30_gr22.tsv',
                            'GH30', "CWDE", "L22")

data_GS_19 <- NULL
data_GS_19 <- Import_table(data_GS_19, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/Gluthathione_synt_gr19.tsv',
                             'GS', "FsF", "L19")
data_GS_22 <- NULL
data_GS_22 <- Import_table(data_GS_22, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/Gluthathione_synt_gr22.tsv',
                             'GS', "FsF", "L22")

data_CLE_19 <- NULL
data_CLE_19 <- Import_table(data_CLE_19, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/CLE_gr19.tsv',
                           'CLE', "FsF", "L19")
data_CLE_22 <- NULL
data_CLE_22 <- Import_table(data_CLE_22, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/CLE_gr22.tsv',
                           'CLE', "FsF", "L22")

data_sprysec_19 <- NULL
data_sprysec_19 <- Import_table(data_sprysec_19, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/SPRYSEC_gr19.tsv',
                     'SPRYSEC', "Immune supression", "L19")
data_sprysec_22 <- NULL
data_sprysec_22 <- Import_table(data_sprysec_22, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/SPRYSEC_gr22.tsv',
                                'SPRYSEC', "Immune supression", "L22")

data_1106_22 <- NULL
data_1106_22 <- Import_table(data_1106_22, "~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/1106_gr22.tsv",
                    '1106', 'Immune supression', "L22")

data_1106_19 <- NULL
data_1106_19 <- Import_table(data_1106_19, "~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/1106_gr19.tsv",
                             '1106', 'Immune supression', "L19")


data_GLAND6_22 <- NULL
data_GLAND6_22 <- Import_table(data_GLAND6_22, "~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/GLAND6_gr22.tsv",
                    'GLAND6', 'GLAND6', "L22")
data_GLAND6_19 <- NULL
data_GLAND6_19 <- Import_table(data_GLAND6_19, "~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/GLAND6_gr19.tsv",
                               'GLAND6', 'GLAND6', "L22")

data_GLAND14_22 <- NULL
data_GLAND14_22 <- Import_table(data_GLAND14_22, "~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/GLAND14_gr22.tsv",
                               'GLAND14', 'GLAND14', "L22")

data_GLAND14_19 <- NULL
data_GLAND14_19 <- Import_table(data_GLAND14_19, "~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/GLAND14_gr19.tsv",
                                'GLAND14', 'GLAND14', "L19")


data_all22 <- sapply(list(
  "GH5"= data_GH5_22, "GH30" = data_GH30_22, "CLE" = data_CLE_22, 
  "SPRYSEC" = data_sprysec_22,"1106"=data_1106_22,"GLAND6"=data_GLAND6_22,
  "GLAND14" = data_GLAND14_22),
                     Get_Number_clustered) %>% melt

data_all19 <- sapply(list(
  "GH5"= data_GH5_19, "GH30" = data_GH30_19, "CLE" = data_CLE_19, 
  "SPRYSEC" = data_sprysec_19,"1106"=data_1106_19,"GLAND6"=data_GLAND6_19,
  "GLAND14" = data_GLAND14_19),
  Get_Number_clustered) %>% melt

plt.22 <- ggplot(data_all22, aes(x = Var2, y = value)) +
  geom_col(aes(fill=Var1), position = 'stack') + theme_light() +
  ylab("Number of Genes") + theme(axis.title.x = element_blank()) +
  ggtitle("G. rostochiensis Line 22") + theme(axis.text.x = element_text(angle = 90))

plt.19 <- ggplot(data_all19, aes(x = Var2, y = value)) +
  geom_col(aes(fill=Var1), position = 'stack')  + theme_light() +
  scale_y_continuous( limits = c(0, 100) ) +
  ylab("Number of Genes") + theme(axis.title.x = element_blank()) +
  ggtitle("G. rostochiensis Line 19") + theme(axis.text.x = element_text(angle = 90))


gridExtra::grid.arrange(plt.19, plt.22, ncol = 2)




###########################################
setwd('/home/joris/tools/scripts/gene_families/')
source('Plot_gene_families.R')

comb_table_19 <- rbind(
  data_1106_19, 
  data_GLAND6_19, 
  data_sprysec_19, 
  data_GLAND14_19
)

comb_table_22 <- rbind(
  data_1106_22,
  data_GLAND6_22,
  data_sprysec_22,
  data_GLAND14_22
)

chrom.sizes.22 = read.table("Gr_22.sizes", row.names = 1)
chrom.sizes.19 = read.table("Gr_19.sizes", row.names = 1)

Plot_family_overview(data_1106_19, chrom.sizes.19, title = "G. rostochiensis L19 1106")
Plot_family_overview(data_1106_22, chrom.sizes.22, title = "G. rostochiensis L22 1106")

Plot_family_overview(data_GLAND6_19, chrom.sizes.19, title = "G. rostochiensis L19 4D06")
Plot_family_overview(data_GLAND6_22, chrom.sizes.22, title = "G. rostochiensis L22 4D06")

Plot_family_overview(data_sprysec_19, chrom.sizes.19, title = "G. rostochiensis L19 SPRYSEC")
Plot_family_overview(data_sprysec_22, chrom.sizes.22, title = "G. rostochiensis L22 SPRYSEC")

Plot_family_overview(data_GLAND14_19, chrom.sizes.19, title = "G. rostochiensis L19 GLAND14")
Plot_family_overview(data_GLAND14_22, chrom.sizes.22, title = "G. rostochiensis L22 GLAND14")

Plot_family_overview(comb_table_19, chrom.sizes.19, title = "G. rostochiensis L19")
Plot_family_overview(comb_table_22, chrom.sizes.22, title = "G. rostochiensis L22")