First Mauve was ran using the graphical user interface on the G_rostochiensis_v10_L19_named.fasta, G_rostochiensis_v10_L22_named.fasta and JHI-Ro1 (PRJEB13504) genome assemblies. One of the output files of Mauve (\*.backbone) was used to create the circos plot. This file is formatted as such:

| Line22_leftend | Line22_rightend | Line19_leftend | Line19_rightend | Ro1_leftend | Ro1_rightend |
|----------------|-----------------|----------------|-----------------|-------------|--------------|
| 62390054       | 62390078        | 159601         | 159625          | 0           | 0            |
| 12957132       | 12957142        | 92009573       | 92009583        | 0           | 0            |
| ..             | ..              | ..             | ..              | ..          | ..           |

The backbone file was further processed to remove any links thata are smaller than 3kb. This was done with a custom script()
```
$ python mauve_backbone_to_circos_links.py -i mauve.backbone --threshold 3000 > circos_links_all_3kb.txt
```

A separate link file was generated to highlight regions that are only shared between G_rostochiensis_v10_L19_named.fasta & G_rostochiensis_v10_L22_named.fasta. In practice, those are regions where the JHI-Ro1 genome columns show a start and end of both zero.



Circos requires a file containing the karyotypes. Here we don't strictly use it as karyotypes, but rather show each assembly as one chromosome.
```
chr - line19 Line19 0 92274186  dpurple
chr - line22 Line22 0 101425903 red
chr - ro1 Ro1 0 95876286 grey
band line19 p36.33 p36.33 0 50000000 gneg
band line19 p36.32 p36.32 50000000 92274186 gneg
band line22 p36.33 p36.33 0 50000000 gneg
band line22 p36.32 p36.32 50000000 101425903 gneg
band ro1 p36.33 p36.33 0 50000000 gneg
band ro1 p36.32 p36.32 50000000 95876286 gneg
```

Configuration files used are here and here
