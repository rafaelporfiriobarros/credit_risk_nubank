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
            
            # categorical_features = ["score_3"]

            numerical_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            # categorical_pipeline = Pipeline(
            #     steps = [
            #         ("imputer", SimpleImputer(strategy="most_frequent")),
            #         ("one_hot_encoder", OneHotEncoder()),
            #         ("scaler", StandardScaler(with_mean=False))
            #     ]
            # )
        
            logging.info(f"Numerical Columns: {numerical_features}")
            # logging.info(f"Categorical Columns: {categorical_features}")

            preprocessor = ColumnTransformer(
                [
                    ("numerical_pipeline", numerical_pipeline, numerical_features),
                    # ("categorical_pipeline", categorical_pipeline, categorical_features)
                ]
            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def apply_data_transformation(self, train_path, test_path):

        try:
            train = pd.read_csv(train_path)
            test = pd.read_csv(test_path)

            logging.info("Read train and test sets.")
            logging.info("Obtaining preprocessor object.")

            preprocessor = self.get_preprocessor()

            train["target_default"] = train["target_default"].map({"False":0, "True":1})
            test["target_default"] = test["target_default"].map({"False":0, "True":1})

            target_feature = "target_default"
            to_drop_feature = ["ids", "score_1", "score_2", "reason", "facebook_profile", "state", "zip", "channel", "job_name", "real_state",
            "email", "external_data_provider_first_name", "external_data_provider_email_seen_before","lat_lon", "marketing_channel",
            "application_time_applied", "profile_phone_number", "application_time_in_funnel","shipping_zip_code", "external_data_provider_fraud_score",
            "profile_tags", "user_agent", "target_fraud"]

            train['credit_limit'] = train['credit_limit'].apply(lambda x: np.nan if x == 0 else x)
            test['credit_limit'] = test['credit_limit'].apply(lambda x: np.nan if x == 0 else x)

            train.replace([np.inf, -np.inf], np.nan, inplace=True)
            test.replace([np.inf, -np.inf], np.nan, inplace=True)
            
            train["score_baixo"] = ""
            train["score_medio"] = ""
            train["score_alto"] = ""

            test["score_baixo"] = ""
            test["score_medio"] = ""
            test["score_alto"] = ""


            train.loc[train["score_3"] <= 300 , "baixo"] = "baixo"
            test.loc[test["score_3"] <= 300, "baixo"] = "baixo"

            train.loc[(train["score_3"] >= 301) & (train["score_3"] <= 700), "medio"] = "medio"
            test.loc[(test["score_3"] >= 301) & (test["score_3"] <= 700), "medio"] = "medio"

            train.loc[train["score_3"] >= 701, "alto"] = "alto"
            test.loc[test["score_3"] >= 701, "alto"] = "alto"
            
            # X_train = train.drop(columns = [target_feature, to_drop_feature])
            X_train = train.drop(columns=[target_feature] + to_drop_feature, axis=1)
            y_train = train[target_feature].copy()
            
            X_test = test.drop(columns=[target_feature] + to_drop_feature, axis=1)
            y_test = test[target_feature].copy()

            logging.info("Binarizing Target, dropping Target and irrelevant features from train and test sets. X_train, X_test, y_train, y_test ready for preprocessing.")
            logging.info("Preprocessing train and test sets.")

            X_train_prepared = preprocessor.fit_transform(X_train, y_train)
            X_test_prepared = preprocessor.transform(X_test)

            train_prepared = np.c_[
                X_train_prepared, np.array(y_train)
            ]

            test_prepared = np.c_[
                X_test_prepared, np.array(y_test)
            ]

            logging.info("Entire train and test sets prepared.")
            logging.info("Save preprocessing object.")

            save_object(
                file_path=self.data_transformation_config.preprocessor_file_path,
                obj=preprocessor  # Alterado 'object' para 'obj'
            )

            logging.info("Data ingestion completed.")

            return train_prepared, test_prepared, self.data_transformation_config.preprocessor_file_path

        except Exception as e:
            raise CustomException(e, sys)
        
# if __name__=="__main__":
#     obj=DataTransformation()
#     train_data, test_data = obj.initiate_data_ingestion()

#     data_transformation = DataTransformation()
#     data_transformation.initiate_data_transformation(train_data, test_data)


