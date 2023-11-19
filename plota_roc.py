import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import LabelBinarizer

# Pasta que contém os arquivos CSV
diretorio = 'result/roc'

# Lista de cores para as curvas ROC
cores = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

# Lista para armazenar os dados das curvas ROC
roc_data = []

# Nomes personalizados para os arquivos
nomes_personalizados = ["Arvore de Decisão", "Regressão Logistica", "Naives Bayes", "Rede Neural", "Random Forest"]

# Loop pelos arquivos no diretório
for idx, arquivo in enumerate(os.listdir(diretorio)):
    if arquivo.endswith('.csv'):
        caminho_arquivo = os.path.join(diretorio, arquivo)

        # Carregue os dados do arquivo CSV
        data = pd.read_csv(caminho_arquivo)

        # Suponha que o DataFrame possui colunas 'False Positive Rate', 'True Positive Rate' e 'Thresholds'
        fpr = data['Falso Positivo']
        tpr = data['Verdadeiro Positivo']
        auc_score = auc(fpr, tpr)  # Calcule a AUC

        # Armazene os dados da curva ROC em uma lista
        roc_data.append({'fpr': fpr, 'tpr': tpr, 'nome': f"{nomes_personalizados[idx]} (AUC={auc_score:.2f})"})

# Crie um gráfico único para todas as curvas ROC
plt.figure(figsize=(10, 8))

for data in roc_data:
    plt.plot(data['fpr'], data['tpr'], lw=2, label=data['nome'])

plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Taxa de Falso Positivo', fontsize=11)
plt.ylabel('Taxa de Verdadeiro Positivo', fontsize=11)
plt.title('Curvas ROC-AUC dos Modelos', fontsize=12)
plt.legend(loc='lower right')
# Salvar a figura gerada
plt.savefig('ML/result/curvas_roc.png')

plt.show()