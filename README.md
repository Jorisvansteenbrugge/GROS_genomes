# GROS_genomes

Repository containing commands and scripts to generate the genome assemblies and perform the comparative genomics analyses.
The genome sequence of Gr-Line19 is available under BioSample: **SAMN17613196** and the genome sequence of Gr-Line22 is available under BioSample: **SAMN17613218**

The sequence reads used in this project are available at the NCBI SRA database under BioProject **PRJNA695196**


| NCBI SRA ID     | Spots    | Platform    | Isolate   |
|-------------|----------|-------------|-----------|
| SRR13560389 | 23668331 | ILLUMINA    | Gr-Line19 |
| SRR13560388 | 23544408 | ILLUMINA    | Gr-Line19 |
| SRR13560391 | 23579544 | ILLUMINA    | Gr-Line22 |
| SRR13560390 | 23640685 | ILLUMINA    | Gr-Line22 |
| SRR13560397 | 653296   | PACBIO_SMRT | Gr-Line19 |
| SRR13560396 | 648034   | PACBIO_SMRT | Gr-Line19 |
| SRR13560395 | 701627   | PACBIO_SMRT | Gr-Line19 |
| SRR13560394 | 603883   | PACBIO_SMRT | Gr-Line22 |
| SRR13560393 | 508886   | PACBIO_SMRT | Gr-Line22 |
| SRR13560392 | 560230   | PACBIO_SMRT | Gr-Line22 |


# Assembly pipeline
The detailed pipeline description with the exact commands used is explained in [Assembly/Pipeline.md](Assembly/Pipeline.md). Various custom scripts used in the pipeline are available in the folder [Assembly/](Assembly/)

# Gene predictions
Gene predictions were done as described in [BRAKER_grene_predictions.md](BRAKER_grene_predictions.md)

# Repeat Masking
Masking of repeats is done through RepeatModeler/Repeatmasker using a custom pipeline that is available here: https://github.com/Jorisvansteenbrugge/RepeatMaskPipeline.
The pipeline was run with the following commands:
```
$ mkdir gr19_repeatmask
$ mkdir gr22_repeatmask
$ Repeatmask_pipeline run all --workdir gr19_repeatmask/ -i G_rostochiensis_v10_L19_named.fasta -p 8 
$ Repeatmask_pipeline run all --workdir gr22_repeatmask/ -i G_rostochiensis_v10_L22_named.fasta -p 8 
```
