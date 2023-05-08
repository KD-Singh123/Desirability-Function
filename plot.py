import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define sigmoid functions for PARP1, PARP2, and tankyrase
def parp1(ic50_parp1):
    return (1 / (1 + np.exp(0.22*(ic50_parp1-27.5)))) * ((1 - 0.1) + 0.1)

def parp2(ic50_parp2):
    return (1 / (1 + np.exp(0.0204*(ic50_parp2-255)))) * ((1 - 0.1) + 0.1)

def tankyrase(ic50_tankyrase):
    return (1 / (1 + np.exp(-0.0034*(ic50_tankyrase-1550)))) * ((1 - 0.1) + 0.1)

# Generate input data from CSV file
df = pd.read_csv('input.csv')

# Calculate sigmoid values for each drug and add them to the dataframe
for index, row in df.iterrows():
    UF_parp1 = parp1(row['IC50_parp1'])
    UF_parp2 = parp2(row['IC50_parp2'])
    UF_tankyrase = tankyrase(row['IC50_tankyrase'])
    df.loc[index, 'S_parp1'] = UF_parp1
    df.loc[index, 'S_parp2'] = UF_parp2
    df.loc[index, 'S_tankkyrase'] = UF_tankyrase

# Save output dataframe to CSV file
df.to_csv('output.csv', index=False)

# Plot sigmoid curves for each drug with scatter points
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

for index, ax in enumerate(axs):
    if index == 0:
        x = df['IC50_parp1']
        y = df['S_parp1']
        label = 'PARP1'
        sigmoid_func = parp1
        xlabel = 'IC50_parp1'
    elif index == 1:
        x = df['IC50_parp2']
        y = df['S_parp2']
        label = 'PARP2'
        sigmoid_func = parp2
        xlabel = 'IC50_parp2'
    else:
        x = df['IC50_tankyrase']
        y = df['S_tankkyrase']
        label = 'Tankyrase'
        sigmoid_func = tankyrase
        xlabel = 'IC50_tankyrase'
        
    ax.plot(np.linspace(min(x), max(x), 100), sigmoid_func(np.linspace(min(x), max(x), 100)), color='black', label='Sigmoid Curve')
    ax.scatter(x, y, label=label)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('UF')
    ax.set_title(label)
    ax.legend()

    # Add point labels
    for i, txt in enumerate(df['ID']):
        ax.annotate(txt, (x[i], y[i]))        
#plt.show()
