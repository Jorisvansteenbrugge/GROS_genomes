# Trimming of reads

Since we sequenced a pool of genomes we perform a read correction step to reduce the number of haplotypes in the reads. Canu (https://github.com/marbl/canu) is used for the error correction of the reads. Specifically, parameters these parameters were tweaked: `corOutCoverage=200 correctedErrorRate=0.15`.

```
$ canu -correct -p gr19 -d gr19_corrected_reads genomeSize=100m corOutCoverage=200 correctedErrorRate=0.15 -pacbio-raw SRR13560397.fasta SRR13560396.fasta SRR13560395.fasta
$ canu -correct -p gr22 -d gr22_corrected_reads genomeSize=100m corOutCoverage=200 correctedErrorRate=0.15 -pacbio-raw SRR13560394.fasta SRR13560393.fasta SRR13560392.fasta
```
The corrected reads produced by canu are stored as gr19.correctedReads.fasta.gz and gr22.correctedReads.fasta.gz



# Assembly with wtdgb2

For each genome approximately 100 initial assemblies were produced optimizing the parameters minimal read length, k-mer size, and minimal read depth. This optimization step is performed with a custom script [optimize_wtdbg2.py](https://github.com/Jorisvansteenbrugge/GROS_genomes/blob/main/Assembly/optimize_wtdbg2.py)

```
$ python Assembly/optimize_wtdbg2.py --reads gr19.correctedReads.fasta.gz --wd gr19_initial_assemblies -t 8
$ python Assembly/optimize_wtdbg2.py --reads gr22.correctedReads.fasta.gz --wd gr22_initial_assemblies -t 8
```

The quality of the initial assemblies was assessed based on whether the assembly size was close to the genome size estimate (Eves-van den Akker et al., 2016), and the completeness ([BUSCO](https://github.com/Jorisvansteenbrugge/GROS_genomes/blob/main/BUSCO.md)). For Gr-Line19 Assembly_L6000_p20e5 was selected to continue, for Gr-Line22 Assembly_L5000p15e6 was selected to continue.
