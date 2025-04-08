import os
import sys

import numpy as np 
import pandas as pd
import dill
import pickle

# Data manipulation and visualization.
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Modelling.
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix, roc_curve, precision_recall_curve
import time

# Debugging.
from exception import CustomException
from logger import logging
import sys

# Warnings.
from warnings import filterwarnings
filterwarnings('ignore')

from exception import CustomException

# Essa função salva um objeto Python em um arquivo.
def save_object(file_path, obj):
    try:
        # Obtenção do diretório do arquivo
        # file_path é o caminho completo onde o objeto será salvo.
        dir_path = os.path.dirname(file_path) # extrai apenas o diretório do caminho.

        # Criação do diretório, se necessário
        # Se o diretório dir_path não existir, ele será criado.
        # O parâmetro exist_ok=True evita erro se o diretório já existir.
        os.makedirs(dir_path, exist_ok=True)

        # Salvamento do objeto com pickle
        # Abre o arquivo file_path no modo binário de escrita ("wb").
        # pickle.dump(obj, file_obj): serializa e salva obj no arquivo.
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    # Tratamento de erros
    # Se ocorrer qualquer erro, ele é capturado e lançado como uma CustomException, 
    # provavelmente para melhorar o rastreamento do erro.
    except Exception as e:
        raise CustomException(e, sys)
    

def evaluate_models_cv(models, X_train, y_train):
    try:
        n_folds = 5
        stratified_kfold = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=42)

        # Dictionaries with validation and training scores of each model for plotting further.
        models_val_scores = dict()
        models_train_scores = dict()

        for model in models:
            # Getting the model object from the key with his name.
            model_instance = models[model]

            # Measuring training time.
            start_time = time.time()
            
            # Fitting the model to the training data.
            model_instance.fit(X_train, y_train)

            end_time = time.time()
            training_time = end_time - start_time

            # Make predictions on training data and evaluate them.
            y_train_pred = model_instance.predict(X_train)
            train_score = roc_auc_score(y_train, y_train_pred)

            # Evaluate the model using k-fold cross validation, obtaining a robust measurement of its performance on unseen data.
            val_scores = cross_val_score(model_instance, X_train, y_train, scoring='roc_auc', cv=stratified_kfold)
            avg_val_score = val_scores.mean()
            val_score_std = val_scores.std()

            # Adding the model scores to the validation and training scores dictionaries.
            models_val_scores[model] = avg_val_score
            models_train_scores[model] = train_score

            # Printing the results.
            print(f'{model} results: ')
            print('-'*50)
            print(f'Training score: {train_score}')
            print(f'Average validation score: {avg_val_score}')
            print(f'Standard deviation: {val_score_std}')
            print(f'Training time: {round(training_time, 5)} seconds')
            print()

    
    except Exception as e:
        raise CustomException(e, sys)
    
    def load_object(file_path):
        try:
            with open(file_path, "rb") as file_obj:
                return pickle.load(file_obj)

        except Exception as e:
            raise CustomException(e, sys)
        
logging.info("Utils concluído.")