# Bibliotecas

# os e sys: usados para manipular arquivos e diretórios no sistema operacional.
import os
import sys

import numpy as np
import pandas as pd

# uma alternativa ao pickle que pode serializar mais tipos de objetos (não está sendo usado no código).
import dill

# biblioteca usada para serializar e desserializar objetos Python.
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

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