import pandas as pd
import json
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
import sys
import wandb
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def read_json_file2(file_path):
    with open(file_path, "r") as f:
        return [json.loads(line) for line in f]

# AverageLinearSpeed: alpha 0.1, lr: 0.001, max_iter 200, hiden_layer_sizes: [30, 30, 30]
# AverageMass: alpha 0.1, lr: 0.01, "adaptive", hidden_layer_sizes": {"desc": null,"value": [30,30,30]}, max_iter 200
# AverageVariance: alpha 0.001, lr: 0.001, lr adaptive, max_iter 200, "hidden_layer_sizes": {"desc": null,"value": [30,50,30,50,30]},

# Carica i dati
results4 = pd.DataFrame(read_json_file2("src/masstestClassifier2_LowFiltered_200iterations.json"))

kernels = results4['kernels']
columns = ['kernels', 'ColorR', 'ColorG', 'ColorB', 'massR',
            'massG', 'massB', 'name', 'T', 'R', 'mass', 'variance', 
            'averageLinearSpeed', 'averageVariance', 'averageVarianceSpeed', 
            'averageAngleSpeed', 'averageMass', 'averageAngleSpeedLowFiltered',
       'averageLinearSpeedLowFiltered', 'averageVarianceSpeedLowFiltered']

out = ['averageLinearSpeed', 'averageVariance', 'averageMass']
training_parameter_batch = [{"max_iter":200,"out_column": "averageVarianceSpeedLowFiltered", "alpha": 0.1, "learning_rate_init": 0.01, "tag": "AAS", "hidden_layer_sizes":(30,30,30),"learning_rate": "adaptive"},
                            ]
for batch in training_parameter_batch:
    out_column = batch['out_column']
    # Inizializza una run su W&B
    wandb.init(project="Lenia", name=out_column, config={
        "learning_rate": "adaptive",
        "learning_rate_init": batch['learning_rate_init'],
        "alpha": batch['alpha'],
        "hidden_layer_sizes": batch['hidden_layer_sizes'],
        "max_iter": batch['max_iter']}, 
        tags=[batch['tag']],
        )

    columns_without_output = columns.copy()
    columns_without_output.pop(columns_without_output.index(out_column))

    results4_cleaned = results4.drop(columns=columns_without_output)

    # Funzione per estrarre i valori 'm', 's' e 'h' dai kernel
    def extract_kernel_values(kernel_list):
        values = {}
        for i, kernel in enumerate(kernel_list):
            values[f'm{i}'] = kernel.get('m', None)
            values[f's{i}'] = kernel.get('s', None)
            values[f'h{i}'] = kernel.get('h', None)
        return values

    # Applica la funzione a ogni riga del DataFrame
    kernel_values = kernels.apply(extract_kernel_values)

    # Converti la lista di dizionari in un DataFrame
    kernel_values_df = pd.DataFrame(kernel_values.tolist())
    results4_concat = pd.concat([results4_cleaned, kernel_values_df], axis=1)

    '''Dataset sampling'''
    dataset = results4_concat.sample(frac=1, ignore_index=True) # mescola il campione nel set di addestramento

    mean = dataset.mean()[1:]
    std = dataset.std()[1:]

    TRAIN_TEST_SPLIT_PERCENTAGE = 0.9
    dataset_training = dataset[:int(len(dataset) * TRAIN_TEST_SPLIT_PERCENTAGE)]
    dataset_test = dataset[int(len(dataset) * TRAIN_TEST_SPLIT_PERCENTAGE):]

    # Separare le caratteristiche (X) e il target (y)
    X = dataset_training.drop(columns=[out_column])  # tutte le colonne tranne out_string
    y = dataset_training[out_column]  # solo la colonna out_string

    # Lo stesso per il set di test
    X_test = dataset_test.drop(columns=[out_column])
    y_test = dataset_test[out_column]

    "normalizzazione"
    X = (X - mean) / std
    X_test = (X_test - mean) / std

    "colonna bias"
    X_test['bias'] = 1
    X['bias'] = 1

    # Crea il modello MLPClassifier
    mlp = MLPRegressor(hidden_layer_sizes=batch['hidden_layer_sizes'], max_iter=batch['max_iter'], random_state=42, 
                    learning_rate=batch['learning_rate'], alpha=batch['alpha'], learning_rate_init=batch['learning_rate_init'])

    # Addestra il modello con una barra di progresso e registra su W&B
    for i in range(mlp.max_iter):
        mlp.partial_fit(X, y)
        training_results = mlp.score(X, y)
        testing_results = mlp.score(X_test, y_test)

        # Registra i dati su W&B
        wandb.log({
            "epoca": i, 
            "training_score": training_results, 
            "testing_score": testing_results, 
            "loss": mlp.loss_, 
        })
        sys.stdout.write(f"\rModel for {out_column} is training: {i}/{mlp.max_iter} | Test score: {testing_results:.4f} | Model score: {training_results:.4f}")
        sys.stdout.flush()

    # Termina la run su W&B
    wandb.finish()
