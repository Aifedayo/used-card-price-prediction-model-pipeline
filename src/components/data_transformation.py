import os
import sys
import json
import joblib
from dataclasses import dataclass
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        Creates a LabelEncoder for Leather_interior column and a scaler
        for the Mileage
        """
        try:
            scaler = StandardScaler()
            le = LabelEncoder()
            return scaler, le

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path: str, test_path: str):
        """
        Reads the training and testing data, applies transformations, 
        and saves the preprocessor object.
        """
        try:
            # Load datasets
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Reading train and test data completed.")

            # Get the preprocessing object and the columns
            mileage_scaler, le = self.get_data_transformer_object()

            # Apply transformations on train and test data
            train_df['Mileage'] = pd.to_numeric(train_df['Mileage'], errors='coerce')
            test_df['Mileage'] = pd.to_numeric(test_df['Mileage'], errors='coerce')

            scaled_train_mileage = mileage_scaler.fit_transform(train_df[['Mileage']])
            train_df['Mileage'] = scaled_train_mileage
            joblib.dump(mileage_scaler, 'artifacts/mileage_scaler.pkl')
            scaled_test_mileage = mileage_scaler.transform(test_df[['Mileage']])
            test_df['Mileage'] = scaled_test_mileage

            train_df['Leather_interior'] = le.fit_transform(train_df['Leather_interior'])
            test_df['Leather_interior'] = le.transform(test_df['Leather_interior'])
            train_df['Leather_interior'] = train_df['Leather_interior'].astype('category')
            test_df['Leather_interior'] = test_df['Leather_interior'].astype('category')

            logging.info("Applied the preprocessing object on the training and testing dataframes.")

            for col in train_df.select_dtypes(include=['object']).columns:
                train_df[col] = train_df[col].astype('category')

            for col in test_df.select_dtypes(include=['object']).columns:
                test_df[col] = test_df[col].astype('category')

            return (
                train_df, test_df, self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)
