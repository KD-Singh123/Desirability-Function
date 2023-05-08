import csv
import numpy as np
import pandas as pd
import base64
import math
def parp1(ic50_parp1):
    return (1 / (1 + np.exp(0.22*(ic50_parp1-27.5)))) * ((1 - 0.1) + 0.1)
def parp2(ic50_parp2):
    return (1 / (1 + np.exp(0.0204*(ic50_parp2-255)))) * ((1 - 0.1) + 0.1)
def tankyrase(ic50_tankyrase):
    return (1 / (1 + np.exp(-0.0034*(ic50_tankyrase-1550)))) * ((1 - 0.1) + 0.1)
def CYP(ic50_CYP):
    if ic50_CYP >= 10:
        return 1
    else:
        return 0
def hERG(ic50_hERG):
    if ic50_hERG >= 10:
        return 1
    else:
        return 0
def final_score(ic50_parp1, ic50_parp2, ic50_tankyrase, ic50_hERG, ic50_CYP):
    score = parp1(ic50_parp1) * parp2(ic50_parp2) * tankyrase(ic50_tankyrase) * hERG(ic50_hERG) * CYP(ic50_CYP)
    return score
def d_final_score(score):
    if score >= 0.5:
        return "Desirable"
    else:
        return "Undesirable"
df = pd.read_csv('input.csv')
for index, row in df.iterrows():
    UF_parp1 = parp1(row['IC50_parp1'])
    UF_parp2 = parp2(row['IC50_parp2'])
    UF_tankyrase = tankyrase(row['IC50_tankyrase'])
    UF_hERG = hERG(row['IC50_hERG'])
    UF_CYP = CYP(row['IC50_CYP'])
    final_score_value = final_score(row['IC50_parp1'], row['IC50_parp2'], row['IC50_tankyrase'], row['IC50_hERG'], row['IC50_CYP'])
    desirability_value = d_final_score(final_score_value) 
    df.loc[index, 'S_parp1'] = UF_parp1
    df.loc[index, 'S_parp2'] = UF_parp2
    df.loc[index, 'S_tankkyrase'] = UF_tankyrase
    df.loc[index, 'S_hERG'] = UF_hERG
    df.loc[index, 'S_CYP'] = UF_CYP
    df.loc[index, 'Final_score'] = final_score_value
    df.loc[index, 'Desirability'] = desirability_value
df.to_csv('output.csv', index=False)
