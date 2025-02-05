import sys
import os
import numpy as np
import pandas as pd
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler, OneHotEncoder
from category_encoders import TargetEncoder
from exception import CustomException
from logger import logging
from utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_file_path: str = os.path.join("artifacts", "preprocessor.pkl")
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "data.csv")

class DataTransformation:
    def __init__(self) -> None:
        self.data_transformation_config = DataTransformationConfig()
        self.numerical_features = [
            "risk_rate", "score_3", "last_amount_borrowed", "last_borrowed_in_months",
            "credit_limit", "income", "ok_since", "n_bankruptcies",
            "n_defaulted_loans", "n_accounts", "n_issues",
            "external_data_provider_credit_checks_last_2_year",
            "external_data_provider_credit_checks_last_month",
            "external_data_provider_credit_checks_last_year", "reported_income"
        ]
        self.categorical_columns = ["score"]
        self.columns_to_drop = [
            "ids", "score_1", "score_2", "reason", "facebook_profile", "state", "zip", "channel", "job_name", "real_state",
            "email", "external_data_provider_first_name", "external_data_provider_email_seen_before", "lat_lon", "marketing_channel",
            "application_time_applied", "profile_phone_number", "application_time_in_funnel", "shipping_zip_code", "external_data_provider_fraud_score",
            "profile_tags", "user_agent", "shipping_state", "target_fraud"
        ]

    def get_preprocessor(self):
        """Cria e retorna um pré-processador para dados numéricos e categóricos."""
        try:
            numerical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            categorical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            logging.info(f"Colunas Numéricas: {self.numerical_features}")
            logging.info(f"Colunas Categóricas: {self.categorical_columns}")

            preprocessor = ColumnTransformer(
                transformers=[
                    ("numerical_pipeline", numerical_pipeline, self.numerical_features),
                    ("categorical_pipeline", categorical_pipeline, self.categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def convert_boolean_to_int(self, df, column_name):
        """Converte valores booleanos para inteiros (0 ou 1)."""
        if column_name in df.columns:
            df[column_name] = df[column_name].fillna(False).astype(int)
        else:
            raise ValueError(f"A coluna '{column_name}' não existe no DataFrame.")
        return df

    def replace_zero_with_nan(self, df, column_name):
        """Substitui valores 0 por NaN em uma coluna específica."""
        df[column_name] = df[column_name].apply(lambda x: np.nan if x == 0 else x)
        return df

    def replace_inf_with_nan(self, df):
        """Substitui valores infinitos por NaN."""
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        return df

    def categorize_score(self, df, column="score_3"):
        """Categoriza a coluna 'score_3' em 'baixo', 'medio' e 'alto'."""
        df["score"] = ""
        df.loc[df[column] <= 300, "score"] = "baixo"
        df.loc[(df[column] >= 301) & (df[column] <= 700), "score"] = "medio"
        df.loc[df[column] >= 701, "score"] = "alto"
        return df

    def prepare_data(self, train, test, target_feature="target_default"):
        """Prepara os dados de treino e teste, separando features e target."""
        X_train = train.drop(columns=[target_feature] + self.columns_to_drop, axis=1)
        y_train = train[target_feature].copy()

        X_test = test.drop(columns=[target_feature] + self.columns_to_drop, axis=1)
        y_test = test[target_feature].copy()

        return X_train, y_train, X_test, y_test

    def apply_data_transformation(self, train_path, test_path):
        """Aplica a transformação de dados nos conjuntos de treino e teste."""
        try:
            train = pd.read_csv(train_path)
            test = pd.read_csv(test_path)

            logging.info("Leitura dos conjuntos de treinamento e teste concluída.")
            logging.info("Obtendo objeto do pré-processador.")

            preprocessor = self.get_preprocessor()

            # Aplicar transformações
            train = self.convert_boolean_to_int(train, "target_default")
            test = self.convert_boolean_to_int(test, "target_default")

            train = self.replace_zero_with_nan(train, "credit_limit")
            test = self.replace_zero_with_nan(test, "credit_limit")

            train = self.replace_inf_with_nan(train)
            test = self.replace_inf_with_nan(test)

            train = self.categorize_score(train)
            test = self.categorize_score(test)

            X_train, y_train, X_test, y_test = self.prepare_data(train, test)

            logging.info("Binarizando Target, removendo Target e recursos irrelevantes dos conjuntos de treinamento e teste.")
            logging.info("Pré-processamento de conjuntos de treinamento e teste.")

            X_train_prepared = preprocessor.fit_transform(X_train, y_train)
            X_test_prepared = preprocessor.transform(X_test)

            train_prepared = np.c_[X_train_prepared, np.array(y_train)]
            test_prepared = np.c_[X_test_prepared, np.array(y_test)]

            logging.info("Conjuntos completos de treino e teste preparados.")
            logging.info("Salvando objeto de pré-processamento.")

            save_object(
                file_path=self.data_transformation_config.preprocessor_file_path,
                obj=preprocessor
            )

            logging.info("Transformação de Dados concluída.")

            return train_prepared, test_prepared, self.data_transformation_config.preprocessor_file_path

        except Exception as e:
            raise CustomException(e, sys)

# Exemplo de uso
# if __name__ == "__main__":
#     obj = DataTransformation()
#     train_data, test_data = obj.initiate_data_ingestion()
#     data_transformation = DataTransformation()
#     data_transformation.apply_data_transformation(train_data, test_data)