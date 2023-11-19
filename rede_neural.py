import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier  # Importe o MLPClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import cross_validate, cross_val_predict
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler, QuantileTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_curve
from sklearn.model_selection import  KFold
import matplotlib.pyplot as plt

# Carregue os dados do arquivo CSV
resultados_rh = pd.read_csv('ML/dados/HR_Artigo.csv')

# Separe os dados em recursos (valores_rh) e a variável alvo (resultado)
valores_rh = resultados_rh.drop(columns=["Attrition"])  # Recursos (todas as colunas, exceto "Attrition")
resultado = resultados_rh.Attrition  # Variável alvo, que é "Attrition"


# Cria um pipeline com etapas para normalização dos dados e classificação com método MinMaxScaler()
#classificador = Pipeline(steps=[
#    ("normalizacao", MinMaxScaler()),
#    ("Classificador", MLPClassifier(alpha=0.01, activation='identity',solver='adam', learning_rate='adaptive', hidden_layer_sizes=(500, 400), max_iter=500, random_state=123143)
#)
#])

# Cria um pipeline com etapas para normalização dos dados e classificação  com método StandardScaler()

classificador = Pipeline(steps=[
    ("normalizacao", StandardScaler()),
    ("Classificador", MLPClassifier(alpha=0.01, activation='identity',solver='adam', learning_rate='adaptive', hidden_layer_sizes=(500, 400), max_iter=500, random_state=123143)
)
])

# Defina as métricas que deseja calcular
scoring = {
    'accuracy': 'accuracy',
    'precision': 'precision',
    'recall': 'recall',
    'f1': 'f1',
    'roc_auc': 'roc_auc'
}

## Realize a validação cruzada com KFold e calcule as métricas separadamente para treino e teste
cv = KFold(n_splits=5, shuffle=True, random_state=None)
train_scores = {metric: [] for metric in scoring}
test_scores = {metric: [] for metric in scoring}

for train_index, test_index in cv.split(valores_rh):
    X_train, X_test = valores_rh.iloc[train_index], valores_rh.iloc[test_index]
    y_train, y_test = resultado.iloc[train_index], resultado.iloc[test_index]

    # Treinamento
    classificador.fit(X_train, y_train)

    # Previsões
    y_train_pred = classificador.predict(X_train)
    y_test_pred = classificador.predict(X_test)

    # Cálculo das métricas
    for metric in scoring:
        if metric == 'roc_auc':
            train_scores[metric].append(roc_auc_score(y_train, classificador.predict_proba(X_train)[:, 1]))
            test_scores[metric].append(roc_auc_score(y_test, classificador.predict_proba(X_test)[:, 1]))
        else:
            train_scores[metric].append(eval(f'{metric}_score')(y_train, y_train_pred))
            test_scores[metric].append(eval(f'{metric}_score')(y_test, y_test_pred))

# Calcule as médias e desvios padrão das métricas após a validação cruzada para treino e teste
train_metric_means = {metric: np.mean(scores) for metric, scores in train_scores.items()}
train_metric_stds = {metric: np.std(scores) for metric, scores in train_scores.items()}
test_metric_means = {metric: np.mean(scores) for metric, scores in test_scores.items()}
test_metric_stds = {metric: np.std(scores) for metric, scores in test_scores.items()}

# Salve as médias e desvios padrão das métricas após a validação cruzada em arquivos CSV
metrics_dict = {
    'Metric': list(scoring.keys()) + [f'Std_{metric}' for metric in scoring.keys()],
    'Train_Mean': list(train_metric_means.values()) + list(train_metric_stds.values()),
    'Test_Mean': list(test_metric_means.values()) + list(test_metric_stds.values())
}

metrics_df = pd.DataFrame(metrics_dict)
metrics_df.to_csv('ML/result/metrics_nn.csv', index=False)

# Realize a validação cruzada com cross_val_predict para obter as probabilidades previstas
y_probas = cross_val_predict(classificador, valores_rh, resultado, cv=cv, method='predict_proba')

# Calcule a curva ROC
fpr, tpr, thresholds = roc_curve(resultado, y_probas[:, 1])

# Salve a curva ROC em um DataFrame do Pandas
roc_data = pd.DataFrame({'Falso Positivo': fpr, 'Verdadeiro Positivo': tpr})

# Salve o DataFrame em um arquivo CSV
roc_data.to_csv('ML/result/metrics_nn_data.csv', index=False)

# Calcule a área sob a curva ROC (ROC-AUC)
roc_auc = roc_auc_score(resultado, y_probas[:, 1])

# Plote a curva ROC
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc='lower right')
plt.show()