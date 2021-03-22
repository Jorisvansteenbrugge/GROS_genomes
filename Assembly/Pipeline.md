# Trimming of reads

Since we sequenced a pool of genomes we perform a read correction step to reduce the number of haplotypes in the reads. Canu (https://github.com/marbl/canu) is used for the error correction of the reads. Specifically, parameters these parameters were tweaked: `corOutCoverage=200 correctedErrorRate=0.15`.

```
$ canu -correct -p gr19 -d gr19_corrected_reads genomeSize=95m corOutCoverage=200 correctedErrorRate=0.15 -pacbio-raw SRR13560397.fasta SRR13560396.fasta SRR13560395.fasta
$ canu -correct -p gr22 -d gr22_corrected_reads genomeSize=95m corOutCoverage=200 correctedErrorRate=0.15 -pacbio-raw SRR13560394.fasta SRR13560393.fasta SRR13560392.fasta
```


