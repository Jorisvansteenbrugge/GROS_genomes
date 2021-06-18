Model selection was carried out using [modeltest](https://github.com/ddarriba/modeltest)

Darriba, D., Posada, D., Kozlov, A. M., Stamatakis, A., Morel, B., & Flouri, T. (2020). ModelTest-NG: a new and scalable tool for the selection of DNA and protein evolutionary models. Molecular Biology and Evolution, 37(1), 291-294. doi.org/10.1093/molbev/msz189



## Gr-1106
```
$ modeltest-ng -i 1106_codingseqs.nexus.reduced
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
The reccomended raxmlHPC-SSE3 command with the optimal model  was suggested as `raxmlHPC-SSE3 -s 1106_codingseqs.nexus.reduced -m GTRGAMMAX -n EXEC_NAME -p PARSIMONY_SEED`
