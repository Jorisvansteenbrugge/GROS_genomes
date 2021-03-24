# Phylogenetic analysis

For phylogeny, the CDS in fasta format were aligned (MSA)  with Muscle (https://www.ebi.ac.uk/Tools/msa/muscle/) ans stored in nexus/phylip format.


The MSA was then used in RaxML (https://pubmed.ncbi.nlm.nih.gov/24451623/) 

```
$ raxmlHPC-PTHREADS-AVX -T 10 -n SPRYSEC_CDS_V10 -s SPRYSEC_codingseqs.nexus -m GTRGAMMA -p 2831 -x 2424 -k -N 100 -f a
```
