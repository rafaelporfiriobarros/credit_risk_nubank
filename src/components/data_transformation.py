import sys
from exception import CustomException
from logger import logging

import os 

import numpy as np
import pandas as pd
from dataclasses import dataclass

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler, OneHotEncoder
from category_encoders import TargetEncoder

from utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_file_path = os.path.join("artifacts", "preprocessor.pkl")
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")


class DataTransformation:
    def __init__(self) -> None:
        self.data_transformation_config = DataTransformationConfig()
    
    def get_preprocessor(self):
        try:
            numerical_features = [  "risk_rate", "score_3", "last_amount_borrowed", "last_borrowed_in_months",
                                    "credit_limit", "income", "ok_since", "n_bankruptcies",
                                    "n_defaulted_loans", "n_accounts", "n_issues",
                                    "external_data_provider_credit_checks_last_2_year",
                                    "external_data_provider_credit_checks_last_month",
                                    "external_data_provider_credit_checks_last_year", "reported_income"]
            
            categorical_columns = ["score"]
        

            numerical_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            categorical_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            logging.info(f"Colunas Numericas: {numerical_features}")
            logging.info(f"Colunas Categoricas: {categorical_columns}")

            preprocessor = ColumnTransformer(
                [
                    ("numerical_pipeline", numerical_pipeline, numerical_features),
                    ("categorical_pipeline",categorical_pipeline,categorical_columns)
                ]
            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def apply_data_transformation(self, train_path, test_path):

        try:
            train = pd.read_csv(train_path)
            test = pd.read_csv(test_path)

            logging.info("Ler conjuntos de treinamento e teste.")
            logging.info("Obtendo objeto do pre-processador.")

            preprocessor = self.get_preprocessor()

            ################################ Funções ################################

            # função para converter valores boolean para int
            def convert_boolean_to_int(df, column_name):
                if column_name in df.columns:
                    df[column_name] = df[column_name].fillna(False).astype(int)
                else:
                    raise ValueError(f"A coluna '{column_name}' não existe no Dataframe.")
                return df
            
            train = convert_boolean_to_int(train, "target_default")
            test = convert_boolean_to_int(test, "target_default")

            ################################################################################################

            # função para substituir valores com 0 para nan
            def replace_zero_with_nan(df, column_name):
                df[column_name] = df[column_name].apply(lambda x: np.nan if x == 0 else x)
                return df
            
            train = replace_zero_with_nan(train, "credit_limit")
            test = replace_zero_with_nan(test, "credit_limit")

            ################################################################################################

            # função para substituir valores inf e -inf para nan
            def replace_inf_with_nan(df):
                df.replace([np.inf, -np.inf], np.nan, inplace=True)
                return df
            
            train = replace_inf_with_nan(train)
            test = replace_inf_with_nan(test)

            ################################################################################################

            # função para categorizar o score_3
            def categorize_score(df, column="score_3"):
                df["score"] = ""
                df.loc[df[column] <= 300, "score"] = "baixo"
                df.loc[(df[column] >= 301) & (df[column] <= 700), "score"] = "medio"
                df.loc[df[column] >= 701, "score"] = "alto"
                
                return df
            
            train = categorize_score(train)
            test = categorize_score(test)

                

            # função para separar os dados de treino em features (x) e target (y)
            def prepare_data(train, test, target_feature="target_default", to_drop_feature=None):
                if to_drop_feature is None:
                    to_drop_feature = ["ids", "score_1", "score_2", "reason", "facebook_profile", "state", "zip", "channel", "job_name", "real_state",
                                    "email", "external_data_provider_first_name", "external_data_provider_email_seen_before","lat_lon", "marketing_channel",
                                    "application_time_applied", "profile_phone_number", "application_time_in_funnel","shipping_zip_code", "external_data_provider_fraud_score",
                                    "profile_tags", "user_agent", "shipping_state","target_fraud"]

                # Preparar dados de treino
                X_train = train.drop(columns=[target_feature] + to_drop_feature, axis=1)
                y_train = train[target_feature].copy()

                # Preparar dados de teste
                X_test = test.drop(columns=[target_feature] + to_drop_feature, axis=1)
                y_test = test[target_feature].copy()

                return X_train, y_train, X_test, y_test


            X_train, y_train, X_test, y_test = prepare_data(train, test)

            ################################################################################################

            logging.info("Binarizando Target, removendo Target e recursos irrelevantes dos conjuntos de treinamento e teste. X_train, X_test, y_train, y_test prontos para pre-processamento.")
            logging.info("Pre-processamento de conjuntos de treinamento e teste.")

            X_train_prepared = preprocessor.fit_transform(X_train, y_train)
            X_test_prepared = preprocessor.transform(X_test)

            train_prepared = np.c_[
                X_train_prepared, np.array(y_train)
            ]

            test_prepared = np.c_[
                X_test_prepared, np.array(y_test)
            ]

            logging.info("Conjuntos completos de trem e teste preparados.")
            logging.info("Salvar objeto de pre-processamento.")

            save_object(
                file_path=self.data_transformation_config.preprocessor_file_path,
                obj=preprocessor  # Alterado 'object' para 'obj'
            )

            logging.info("Ingestao dos Dados completada.")

            return train_prepared, test_prepared, self.data_transformation_config.preprocessor_file_path

        except Exception as e:
            raise CustomException(e, sys)
        
# if __name__=="__main__":
#     obj=DataTransformation()
#     train_data, test_data = obj.initiate_data_ingestion()

#     data_transformation = DataTransformation()
#     data_transformation.initiate_data_transformation(train_data, test_data)


