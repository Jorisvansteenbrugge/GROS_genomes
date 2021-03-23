# Trimming of reads

Since we sequenced a pool of genomes we perform a read correction step to reduce the number of haplotypes in the reads. Canu (https://github.com/marbl/canu) is used for the error correction of the reads. Specifically, parameters these parameters were tweaked: `corOutCoverage=200 correctedErrorRate=0.15`.

```
$ canu -correct -p gr19 -d gr19_corrected_reads genomeSize=100m corOutCoverage=200 correctedErrorRate=0.15 \
    -pacbio-raw SRR13560397.fasta SRR13560396.fasta SRR13560395.fasta
$ canu -correct -p gr22 -d gr22_corrected_reads genomeSize=100m corOutCoverage=200 correctedErrorRate=0.15 \
    -pacbio-raw SRR13560394.fasta SRR13560393.fasta SRR13560392.fasta
```
The corrected reads produced by canu are stored as **gr19.correctedReads.fasta.gz** and **gr22.correctedReads.fasta.gz**



# Assembly with wtdgb2

For each genome approximately 100 initial assemblies were produced optimizing the parameters minimal read length, k-mer size, and minimal read depth. This optimization step is performed with a custom script [optimize_wtdbg2.py](https://github.com/Jorisvansteenbrugge/GROS_genomes/blob/main/Assembly/optimize_wtdbg2.py)

```
$ python Assembly/optimize_wtdbg2.py --reads gr19.correctedReads.fasta.gz --wd gr19_initial_assemblies -t 8
$ python Assembly/optimize_wtdbg2.py --reads gr22.correctedReads.fasta.gz --wd gr22_initial_assemblies -t 8
```

The quality of the initial assemblies was assessed based on whether the assembly size was close to the genome size estimate (Eves-van den Akker et al., 2016), and the completeness ([BUSCO](https://github.com/Jorisvansteenbrugge/GROS_genomes/blob/main/BUSCO.md)). For Gr-Line19 **Assembly_L6000_p20e5** was selected to continue, for Gr-Line22 **Assembly_L5000p15e6** was selected to continue.

# Purging of Haplotigs

**Gr-Line19:**
```
$ cat SRR13560397.fasta SRR13560396.fasta SRR13560395.fasta > Gr19_PB_All.fasta
$ minimap2 -t 4 -ax map-pb Assembly_L6000_p20e5.fasta Gr19_PB_All.fasta --secondary=no | samtools sort -m 30G \
    -@ 2 -o Gr19_Assembly_L6000_p20e5_minimapped_AllPB.bam
$ purge_haplotigs hist -b Gr19_Assembly_L6000_p20e5_minimapped_AllPB.bam -g Assembly_L6000_p20e5.fasta -t 8
$ purge_haplotigs cov -i Gr19_Assembly_L6000_p20e5_minimapped_AllPB.bam.genecov -l 4 -m 15 -h 110
$ purge_haplotigs purge -g Assembly_L6000_p20e5.fasta -c coverage_stats.csv
$ mv curated.fasta G_rostochiensis19_PH.fasta
```

**Gr-Line22:**
```
$ cat SRR13560394.fasta SRR13560393.fasta SRR13560392.fasta > Gr22_PB_All.fasta
$ minimap2 -t 4 -ax map-pb Assembly_L5000p15e6.fasta Gr22_PB_All.fasta --secondary=no | samtools sort -m 30G \
    -@ 2 -o Gr22_Assembly_L5000p15e6_minimapped_AllPB.bam
$ purge_haplotigs hist -b Gr22_Assembly_L5000p15e6_minimapped_AllPB.bam -g Assembly_L5000p15e6.fasta -t 8
$ purge_haplotigs cov -i Gr22_Assembly_L5000p15e6_minimapped_AllPB.bam.genecov -l 4 -m 25 -h 140
$ purge_haplotigs purge -g Assembly_L5000p15e6.fasta -c coverage_stats.csv
$ mv curated.fasta G_rostochiensis22_PH.fasta
```

# Finishing Tool

**Gr-Line19**
```
$ mkdir finisheroutput_gr19
$ ln -s gr19.correctedReads.fasta.gz finisheroutput_gr19/raw_reads.fasta.gz
$ finisherSC.py -par 8 finisheroutput_gr19/ ~/tools/miniconda/bin/mummer
```

**Gr-Line22**
```
$ mkdir finisheroutput_gr22
$ ln -s gr22.correctedReads.fasta.gz finisheroutput_gr22/raw_reads.fasta.gz
$ finisherSC.py -par 8 finisheroutput_gr22/ ~/tools/miniconda/bin/mummer
```


# Scaffolding SSPACE-Longread

**Gr-Line19**
```
$ mkdir scaffolding_gr19
$ SSPACE-LongReadunix.pl -c finisheroutput_gr19/improved3.fasta -p gr19.correctedReads.fasta.gz \
     -t 8 -b scaffolding_gr19/ -o 1000 -g 500 -k1
```

**Gr-Line22**
```
$ mkdir scaffolding_gr22
$ SSPACE-LongReadunix.pl -c finisheroutput_gr22/improved3.fasta -p gr22.correctedReads.fasta.gz \
    -t 8 -b scaffolding_gr22/ -o 1000 -g 500 -k1
```

# Gap Filling

**Gr-Line19**
```
$ mkdir gapfilling_gr19
$ minimap2 -t <threads> -Hax map-pb scaffolding_gr19/scaffolds.fasta  gr19.correctedReads.fasta.gz \
    | samtools view -hF 256 - | samtools sort -@ 2 -m 30G -o gapfilling_gr19/correctedreads_onScaffolds.bam - 
$ samtools index gapfilling_gr19/correctedreads_onScaffolds.bam
$ Hydraslayer -o gapfilling_gr19/Gr19_scaffolds_gapfilled.fasta -c 10 -a 60 scaffolding_gr19/scaffolds.fasta \
    gapfilling_gr19/correctedreads_onScaffolds.bam
```

**Gr-Line22**
```
$ mkdir gapfilling_gr22
$ minimap2 -t <threads> -Hax map-pb scaffolding_gr22/scaffolds.fasta  gr22.correctedReads.fasta.gz \
    | samtools view -hF 256 - | samtools sort -@ 2 -m 30G -o gapfilling_gr22/correctedreads_onScaffolds.bam - 
$ samtools index gapfilling_gr22/correctedreads_onScaffolds.bam
$ Hydraslayer -o gapfilling_gr22/Gr22_scaffolds_gapfilled.fasta -c 10 -a 60 scaffolding_gr22/scaffolds.fasta \
    gapfilling_gr22/correctedreads_onScaffolds.bam
```

# Polishing with Arrow

For **Gr-Line19**, the following is repeated three times. The first run uses the output of the gapfilling step `gapfilling_gr19/Gr19_scaffolds_gapfilled.fasta`. The second and third run use the output fasta file of the first and second run, respectively.
```
$ mkdir gr19_Arrow
$ blasr Gr19_PB_All.fasta gapfilling_gr19/Gr19_scaffolds_gapfilled.fasta --out gr19_Arrow/R1.bam --bam --bestn 10 \
        --minMatch 12 --maxMatch 30 --nproc 8 --minSubreadLength 50 --minAlnLength 50 --minPctSimilarity 70 \
        --minPctAccuracy 70 --hitPolicy randombest --randomSeed 1
$ samtools sort gr19_Arrow/R1.bam -@ 2 -m 30G -o gr19_Arrow/R1_sort.bam
$ pbindex gr19_Arrow/R1_sort.bam
$ arrow gr19_Arrow/R1_sort.bam -j 8 --referenceFilename gapfilling_gr19/Gr19_scaffolds_gapfilled.fasta -o gr19_Arrow/Gr19_scaffolds_gapfilled_arrow1.fasta -o gr19_Arrow/Gr19_scaffolds_gapfilled_arrow1.gff -o gr19_Arrow/Gr19_scaffolds_gapfilled_arrow1.fastq
```

For **Gr-Line22**, the following is repeated three times. The first run uses the output of the gapfilling step `gapfilling_gr22/Gr22_scaffolds_gapfilled.fasta`. The second and third run use the output fasta file of the first and second run, respectively.
```
$ mkdir gr22_Arrow
$ blasr Gr22_PB_All.fasta gapfilling_gr22/Gr22_scaffolds_gapfilled.fasta --out gr22_Arrow/R1.bam --bam --bestn 10 \
        --minMatch 12 --maxMatch 30 --nproc 8 --minSubreadLength 50 --minAlnLength 50 --minPctSimilarity 70 \
        --minPctAccuracy 70 --hitPolicy randombest --randomSeed 1
$ samtools sort gr22_Arrow/R1.bam -@ 2 -m 30G -o gr22_Arrow/R1_sort.bam
$ pbindex gr22_Arrow/R1_sort.bam
$ arrow gr22_Arrow/R1_sort.bam -j 8 --referenceFilename gapfilling_gr22/Gr22_scaffolds_gapfilled.fasta -o gr22_Arrow/Gr22_scaffolds_gapfilled_arrow2.fasta -o gr22_Arrow/Gr22_scaffolds_gapfilled_arrow2.gff -o gr22_Arrow/Gr22_scaffolds_gapfilled_arrow2.fastq
```


## Polishing with Pilon

**Gr-Line19**
```
$ mkdir gr19_pilon
$ pilonAuto -g gr19_Arrow/Gr19_scaffolds_gapfilled_arrow3.fasta -m 100 -t 8 -1 SRR13560388_1.fastq SRR13560388_1.fastq \
        -2 SRR13560389_2.fastq SRR13560389_2.fastq -it 5 --pilon pilon-1.23.jar -o gr19_pilon/
```

**Gr-Line22**
```
$ mkdir gr22_pilon
$ pilonAuto -g gr22_Arrow/Gr22_scaffolds_gapfilled_arrow3.fasta -m 100 -t 8 -1 SRR13560388_1.fastq SRR13560388_1.fastq \
        -2 SRR13560389_2.fastq SRR13560389_2.fastq -it 5 --pilon pilon-1.23.jar -o gr22_pilon/
```

## Cleanup
After multiple rounds of polishing with arrow and pilon, the scaffold names tend to get messy; e.g. > Scaffold1|Arrow|Arrow|Arrow|Pilon|Pilon|Pilon|Pilon|Pilon so a custom script was used to generate simple and clean Scaffold names.

```
$ python swap_fasta_header.py Gr19_v10_Scaffold gr19_pilon/round4/pilon_run4.fasta > G_rostochiensis_v10_L19_named.fasta
$ python swap_fasta_header.py Gr22_v10_Scaffold gr22_pilon/round4/pilon_run4.fasta > G_rostochiensis_v10_L22_named.fasta
```
