import sys
from exception import CustomException
from logger import logging

import os

import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from components.data_transformation import DataTransformationConfig
from components.data_transformation import DataTransformation

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

@dataclass
class DataIngestionConfig:
    train_data_path = os.path.join("artifacts", "train.csv")
    test_dat_path = os.path.join("artifacts", "test.csv")
    raw_data_path = os.path.join("artifacts", "data.csv")

class DataIngestion:
    def __init__(self) -> None:
        self.ingestion_config = DataIngestionConfig()

    def apply_data_ingestion(self):
        logging.info("Data ingestion started.")

        try:
            df = pd.read_csv("notebooks/data/acquisition_train.csv")
            logging.info("Read the dataset as a Pandas Dataframe.")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index = False, header = True)

            X = df.drop(columns=["target_default"])
            y = df["target_default"].copy()

            logging.info("Train test split started.")
            X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42)

            train = pd.concat([X_train, y_train], axis=1)
            test = pd.concat([X_test, y_test], axis = 1)

            train.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test.to_csv(self.ingestion_config.test_dat_path, index=False, header=True)

            logging.info("Finished data ingestion.")

            return self.ingestion_config.train_data_path, self.ingestion_config.test_dat_path
        
        except Exception as e:
            raise CustomException(e, sys)
        
if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.apply_data_ingestion()

    data_transformation=DataTransformation()
    train_prepared,test_prepared,_=data_transformation.apply_data_transformation(train_data,test_data)
