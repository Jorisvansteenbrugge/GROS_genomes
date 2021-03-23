The prediction of genes in the Gr-Line19 and Gr-Line22 assemblies was done with BRAKER2 (https://github.com/Gaius-Augustus/BRAKER). Gene prediction was supported by publicly available RNAseq data under accesions PRJEB12075, PRJNA274143, PRJNA274143.

RNAseq data was mapped on the reference genomes using hisat2 ():

```
$ hisat2-build -p 8 G_rostochiensis_v10_L19_named.fasta G_rostochiensis_v10_L19_named_hisat.idx
$ hisat2-build -p 8 G_rostochiensis_v10_L22_named.fasta G_rostochiensis_v10_L22_named_hisat.idx

$ mkdir rnaseq
$ for fwd_read in *_1.fastq.gz
$   do
$     read_base=$(basename $fwd_read _1.fastq.gz)
$     hisat2 -x G_rostochiensis_v10_L19_named_hisat.idx -1 $fwd_read -2 "$read_base"_2.fastq.gz --dta -p 8 \
        | samtools sort -@ 2 -m 30G -o rnaseq/"$read_base"_gr19.bam
$     hisat2 -x G_rostochiensis_v10_L22_named_hisat.idx -1 $fwd_read -2 "$read_base"_2.fastq.gz --dta -p 8 \
        | samtools sort -@ 2 -m 30G -o rnaseq/"$read_base"_gr22.bam
$     samtools index rnaseq/"$read_base"_gr19.bam         
$     samtools index rnaseq/"$read_base"_gr22.bam         
$   done
```

Gene prediction was done using Braker2:

```
$ braker.pl --genome=G_rostochiensis_v10_L19_named.fasta --species=G_rostochiensis_v10_L19 --cores=10 --gff3  --bam=rnaseq/ERR1173511.bam,rnaseq/ERR1173512.bam,rnaseq/ERR202479.bam,rnaseq/ERR202487.bam,rnaseq/PRJNA274143.bam,rnaseq/SRR1873812.bam,rnaseq/SRR1873813.bam,rnaseq/SRR1873814.bam,rnaseq/SRR1873815.bam,rnaseq/SRR1873816.bam,rnaseq/SRR1873817.bam,rnaseq/SRR1873818.bam,rnaseq/SRR1873819.bam,rnaseq/SRR1873820.bam,rnaseq/SRR1873821.bam,rnaseq/SRR1873822.bam,rnaseq/SRR1873823.bam,rnaseq/SRR1873824.bam,rnaseq/SRR1873825.bam,rnaseq/SRR1873826.bam,rnaseq/SRR1873827.bam,rnaseq/SRR1873828.bam,rnaseq/SRR1873829.bam,rnaseq/SRR7167828.bam,rnaseq/SRR7167829.bam 

$ braker.pl --genome=G_rostochiensis_v10_L22_named.fasta --species=G_rostochiensis_v10_L22 --cores=10 --gff3  --bam=rnaseq/ERR1173511.bam,rnaseq/ERR1173512.bam,rnaseq/ERR202479.bam,rnaseq/ERR202487.bam,rnaseq/PRJNA274143.bam,rnaseq/SRR1873812.bam,rnaseq/SRR1873813.bam,rnaseq/SRR1873814.bam,rnaseq/SRR1873815.bam,rnaseq/SRR1873816.bam,rnaseq/SRR1873817.bam,rnaseq/SRR1873818.bam,rnaseq/SRR1873819.bam,rnaseq/SRR1873820.bam,rnaseq/SRR1873821.bam,rnaseq/SRR1873822.bam,rnaseq/SRR1873823.bam,rnaseq/SRR1873824.bam,rnaseq/SRR1873825.bam,rnaseq/SRR1873826.bam,rnaseq/SRR1873827.bam,rnaseq/SRR1873828.bam,rnaseq/SRR1873829.bam,rnaseq/SRR7167828.bam,rnaseq/SRR7167829.bam 
```
