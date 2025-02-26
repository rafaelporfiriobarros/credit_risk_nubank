# File handling.
import os
from dataclasses import dataclass

# Debugging and verbose.
import sys
from exception import CustomException
from logger import logging

# Modelling.
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# Utils.
from utils import save_object

from scipy.stats import randint, uniform

@dataclass
class ModelTrainerConfig:


    model_file_path = os.path.join('artifacts', 'model.pkl')


class ModelTrainer:


    def __init__(self) -> None:

        self.model_trainer_config = ModelTrainerConfig()
    
    
    def apply_model_trainer(self, train_prepared, test_prepared):

        try:
            logging.info('Split train and test prepared arrays.')
            
            X_train_prepared, X_test_prepared, y_train, y_test = train_prepared[:, :-1], test_prepared[:, :-1], train_prepared[:, -1], test_prepared[:, -1]

            logging.info('Started to train the best Random Forest model with the best hyparameters found in modelling step using stratified k-fold cross validation along with bayesian optimization.')

            best_model = RandomForestClassifier(n_estimators= randint(100, 1000),  # Número de árvores na floresta
                                                max_depth= [None, 10, 20, 30, 40, 50],  # Profundidade máxima das árvores
                                                min_samples_split= randint(2, 20),  # Número mínimo de amostras para dividir um nó
                                                min_samples_leaf= randint(1, 20),   # Número mínimo de amostras em uma folha
                                                max_features= ["auto", "sqrt", "log2"],  # Número de features para considerar ao buscar a melhor divisão
                                                bootstrap= [True, False],  # Se as amostras são bootstrapadas ao construir árvores
                                                class_weight= ["balanced"])  # Já definido como "balanced"

            best_model.fit(X_train_prepared, y_train)

            logging.info('Saving the best model.')

            save_object(
                file_path=self.model_trainer_config.model_file_path,
                object=best_model
            )

            logging.info('Best model classification report and roc-auc score on test set returned.')

            final_predictions = best_model.predict(X_test_prepared)
            
            class_report = classification_report(y_test, final_predictions)
            auc_score = roc_auc_score(y_test, final_predictions)

            return class_report, auc_score

        except Exception as e:
            raise CustomException(e, sys)
        
        logging.info("model trainer concluído.")