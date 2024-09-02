import pandas as pd
import json
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def read_json_file2(file_path):
    with open(file_path, "r") as f:
        return [json.loads(line) for line in f]

results4 = pd.DataFrame(read_json_file2("src/masstestClassifier2_LowFiltered_200iterations.json"))

kernels = results4['kernels']
results4 = results4.drop(columns=['kernels', 'name'])

def extract_kernel_values(kernel_list):
    values = {}
    for i, kernel in enumerate(kernel_list):
        values[f'm{i}'] = kernel.get('m', None)
        values[f's{i}'] = kernel.get('s', None)
        values[f'h{i}'] = kernel.get('h', None)
    return values

kernel_values = kernels.apply(extract_kernel_values)

kernel_values_df = pd.DataFrame(kernel_values.tolist())
results4_concat = pd.concat([results4, kernel_values_df], axis=1)

correlation_matrix = results4_concat.corr()

plt.figure(figsize=(20, 14))
sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm', vmin=-1, vmax=1, annot_kws={"size": 10})
plt.title('Matrice di Correlazione dei Parametri')
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()  # Aggiunge spaziatura per evitare che le etichette si sovrappongano
plt.show()

    
