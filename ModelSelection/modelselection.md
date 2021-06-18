Model selection was carried out using [modeltest](https://github.com/ddarriba/modeltest)

Darriba, D., Posada, D., Kozlov, A. M., Stamatakis, A., Morel, B., & Flouri, T. (2020). ModelTest-NG: a new and scalable tool for the selection of DNA and protein evolutionary models. Molecular Biology and Evolution, 37(1), 291-294. doi.org/10.1093/molbev/msz189



## Gr-1106
```
$ modeltest-ng -i 1106_codingseqs.phylip.reduced
```
output summary:
```
Summary:

Partition 1/1:
                         Model         Score        Weight
----------------------------------------------------------
       BIC           TPM3uf+G4     5761.9070        0.4279
       AIC             TIM3+G4     5566.9087        0.4125
      AICc             TIM3+G4     5572.9087        0.4358

```
The reccomended raxmlHPC-SSE3 model was suggested as `GTRGAMMAX`

## Hg-GLAND5
```
$ modeltest-ng -i GLAND5_codingseqs.phylip.reduced
```
output summary:
```
Summary:

Partition 1/1:
                         Model         Score        Weight
----------------------------------------------------------
       BIC            SYM+I+G4    13501.9075        0.1779
       AIC            SYM+I+G4    13216.6742        0.4372
      AICc            SYM+I+G4    13230.6742        0.5539

```
The reccomended raxmlHPC-SSE3 model was suggested as `GTRGAMMAI`

## SPRYSEC
```
$ modeltest-ng -i SPRYSEC_codingseqs.nexus.reduced
```
output summary:
```
Summary:

Partition 1/1:
                         Model         Score        Weight
----------------------------------------------------------
       BIC            TVM+I+G4   175156.9769        0.9038
       AIC            GTR+I+G4   173351.7796        0.6457
      AICc            GTR+I+G4   173421.7796        0.6457
```
The reccomended raxmlHPC-SSe3 model was suggested as `GTRGAMMAX` or `GTRGAMMAIX`

## CLE
```
$ modeltest-ng -i CLE_codingseqs.phylip.reduced
```
output summary:
```
Summary:

Partition 1/1:
                         Model         Score        Weight
----------------------------------------------------------
       BIC           TPM1uf+G4    19249.7019        0.6969
       AIC            TVM+I+G4    18927.6971        0.2796
      AICc            TVM+I+G4    18929.6971        0.2750
```
The reccomended raxmlHPC-SSE3 model was suggested as `GTRGAMMAX` or `GTRGAMMAIX`
