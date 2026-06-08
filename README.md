# 📊 Modelo de Machine Learning para Previsão de Inadimplência

## 📌 Objetivo

Desenvolver um modelo de Machine Learning capaz de prever a probabilidade de inadimplência de clientes utilizando informações cadastrais, financeiras e comportamentais.

O projeto contempla:

- Tratamento e limpeza dos dados;
- Engenharia de atributos;
- Construção de pipelines automatizados;
- Treinamento de múltiplos algoritmos;
- Avaliação utilizando métricas de risco de crédito;
- Interpretação dos resultados;
- Geração de score de crédito.

---

# 🏗️ Arquitetura do Projeto

```text
Dados Brutos
      │
      ▼
Limpeza dos Dados
      │
      ▼
Feature Engineering
      │
      ▼
Train/Test Split
      │
      ▼
Pipeline de Pré-Processamento
      │
      ▼
Treinamento dos Modelos
      │
      ▼
Avaliação (AUC, ROC, KS)
      │
      ▼
Seleção do Melhor Modelo
      │
      ▼
Feature Importance
      │
      ▼
Score de Crédito
```

---

# 📂 Bibliotecas Utilizadas

```python
pandas
numpy
matplotlib
scikit-learn
xgboost
lightgbm
catboost
```

Principais módulos utilizados:

- Pipeline
- ColumnTransformer
- StandardScaler
- OneHotEncoder
- SimpleImputer
- Train Test Split
- ROC Curve
- ROC AUC Score

---

# 📥 Carregamento dos Dados

Os dados são carregados a partir do arquivo:

```python
acquisition_train.csv
```

```python
df = pd.read_csv("./data/acquisition_train.csv")
```

Após a leitura é realizada uma inspeção inicial:

```python
df.info()
```

Objetivos da análise inicial:

- Verificar tipos de dados;
- Identificar valores ausentes;
- Detectar possíveis inconsistências.

---

# 🧹 Limpeza dos Dados

## Tratamento da Variável Target

A variável alvo do problema é:

```python
target_default
```

Conversão para formato numérico:

```python
pd.to_numeric()
```

Remoção de registros sem informação da variável alvo:

```python
dropna(subset=[target])
```

---

## Remoção de Variáveis

Foram removidas colunas consideradas:

- Identificadores únicos;
- Dados pessoais;
- Informações redundantes;
- Variáveis com baixa utilidade preditiva.

Exemplos:

```python
ids
zip
email
user_agent
profile_phone_number
lat_lon
shipping_zip_code
```

Essa etapa reduz ruído e minimiza risco de overfitting.

---

# ⚙️ Engenharia de Atributos

## Debt-to-Income Ratio

Relação entre dívida e renda.

```python
debt_to_income =
last_amount_borrowed / income
```

### Interpretação

Quanto maior o indicador:

- Maior comprometimento financeiro;
- Maior risco de inadimplência.

---

## Credit Utilization

Percentual do limite de crédito utilizado.

```python
credit_utilization =
last_amount_borrowed / credit_limit
```

### Interpretação

Clientes próximos do limite disponível tendem a apresentar maior risco.

---

## Remoção de Variáveis Adicionais

Após a criação dos novos atributos foram removidas algumas variáveis:

```python
income
score_3
score_4
score_5
score_6
```

Objetivo:

- Evitar multicolinearidade;
- Reduzir dimensionalidade.

---

# 🔀 Divisão dos Dados

Separação entre variáveis explicativas e variável alvo.

```python
X = df2.drop(columns=[target])
y = df2[target]
```

---

## Train Test Split

```python
train_test_split(
    test_size=0.30,
    stratify=y,
    random_state=42
)
```

### Configuração

| Conjunto | Percentual |
|-----------|-----------|
| Treino | 70% |
| Teste | 30% |

O parâmetro `stratify=y` preserva a proporção de inadimplentes e adimplentes.

---

# 🔧 Pipeline de Pré-Processamento

## Variáveis Numéricas

```python
SimpleImputer(strategy='median')
StandardScaler()
```

### Etapas

1. Preenchimento de valores faltantes pela mediana;
2. Padronização dos dados.

---

## Variáveis Categóricas

```python
SimpleImputer(strategy='most_frequent')
OneHotEncoder()
```

### Etapas

1. Preenchimento pela categoria mais frequente;
2. Transformação para representação numérica.

---

## Column Transformer

Combina os dois pipelines:

```python
ColumnTransformer()
```

Permitindo que cada tipo de variável receba o tratamento adequado.

---

# 🤖 Modelos Treinados

Foram avaliados diversos algoritmos de classificação.

## Logistic Regression

```python
LogisticRegression(
    max_iter=1000,
    class_weight='balanced'
)
```

### Vantagens

- Simples;
- Interpretável;
- Muito utilizada em scorecards.

---

## Random Forest

```python
RandomForestClassifier(
    n_estimators=200,
    max_depth=8
)
```

### Vantagens

- Captura relações não lineares;
- Reduz overfitting por meio de múltiplas árvores.

---

## Gradient Boosting

```python
GradientBoostingClassifier()
```

### Vantagens

- Excelente capacidade preditiva;
- Bastante utilizado em problemas tabulares.

---

## XGBoost

Modelo baseado em Gradient Boosting otimizado.

### Benefícios

- Alta performance;
- Tratamento robusto de variáveis.

---

## LightGBM

Framework eficiente para grandes volumes de dados.

### Benefícios

- Treinamento rápido;
- Baixo consumo de memória.

---

## CatBoost

Modelo especializado em tratamento de variáveis categóricas.

### Benefícios

- Excelente desempenho em bases heterogêneas;
- Menor necessidade de pré-processamento.

---

# 📈 Avaliação dos Modelos

## ROC AUC

A principal métrica utilizada para comparação dos modelos foi:

```python
roc_auc_score()
```

### Interpretação

| AUC | Qualidade |
|------|------|
| 0.50 | Aleatório |
| 0.60 - 0.70 | Razoável |
| 0.70 - 0.80 | Bom |
| 0.80 - 0.90 | Muito Bom |
| > 0.90 | Excelente |

---

# 📉 Curva ROC

A curva ROC foi construída para todos os modelos.

```python
roc_curve()
```

Objetivo:

Avaliar a capacidade de separação entre:

- Bons clientes;
- Maus clientes.

---

# 📊 Estatística KS

Além do AUC, foi calculada a métrica KS.

```python
KS = max(
| CumGood - CumBad |
)
```

## Interpretação

| KS | Avaliação |
|------|------|
| <20 | Fraco |
| 20-40 | Bom |
| 40-60 | Muito Bom |
| >60 | Excelente |

A métrica KS é amplamente utilizada em:

- Bancos;
- Fintechs;
- Instituições financeiras.

---

# 🏆 Seleção do Melhor Modelo

Os modelos foram classificados de acordo com o AUC.

```python
best_model =
sorted(results,
       key=lambda x:x[1],
       reverse=True)[0]
```

O modelo com maior capacidade discriminatória foi selecionado para produção.

---

# 🔍 Interpretabilidade

## Feature Importance

Para modelos baseados em árvores foi calculada a importância das variáveis.

```python
feature_importances_
```

Objetivos:

- Identificar fatores de risco;
- Explicar decisões do modelo;
- Apoiar áreas de negócio.

---

## SHAP (Opcional)

O projeto já possui estrutura preparada para implementação de SHAP.

Possibilidades:

- Explicações globais;
- Explicações individuais;
- Transparência regulatória.

---

# 🎯 Geração do Score de Crédito

Após o treinamento:

```python
y_pred =
best_pipe.predict_proba(X_test)[:,1]
```

Probabilidade de inadimplência:

```python
prob_default
```

Score calculado:

```python
score = 1000 - (prob_default * 1000)
```

---

## Interpretação do Score

| Score | Risco |
|---------|---------|
| 800 - 1000 | Muito Baixo |
| 600 - 799 | Baixo |
| 400 - 599 | Médio |
| 200 - 399 | Alto |
| 0 - 199 | Muito Alto |

---

# 📋 Métricas Complementares

Também foram calculadas:

```python
precision_score
recall_score
confusion_matrix
classification_report
```

Essas métricas permitem avaliar:

- Precisão;
- Sensibilidade;
- Falsos positivos;
- Falsos negativos.

---

# 🚀 Possíveis Melhorias Futuras

## Modelagem

- Hyperparameter Tuning (Optuna)
- Cross Validation
- Ensemble Learning
- Stacking

## Engenharia de Dados

- Pipeline automatizada com Airflow
- Versionamento com DVC
- Monitoramento de Drift

## MLOps

- MLflow
- Docker
- FastAPI
- Deploy em Cloud

## Interpretabilidade

- SHAP completo
- LIME
- Explainable AI (XAI)

---

# 📌 Conclusão

Este projeto implementa uma solução completa de Credit Scoring utilizando Machine Learning, passando por todas as etapas fundamentais:

- Preparação dos dados;
- Engenharia de atributos;
- Treinamento de múltiplos algoritmos;
- Avaliação por métricas de risco;
- Seleção do melhor modelo;
- Interpretação dos resultados;
- Construção de score de crédito.

O fluxo segue boas práticas utilizadas em áreas de:

- Risco de Crédito;
- Analytics;
- Data Science;
- Fintechs;
- Bancos.