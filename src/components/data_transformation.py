import os
import sys
from dataclasses import dataclass
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self) -> ColumnTransformer:
        """
        Creates and returns a ColumnTransformer object that performs scaling 
        on numerical features and one-hot encoding on categorical features.
        """
        try:
            # Pipeline for scaling numerical features
            numeric_cols = ['Mileage']
            numeric_pipeline = Pipeline(
                steps=[("scaler", StandardScaler())]
            )

            # Pipeline for one-hot encoding categorical features
            leather_interior_cols = ['Leather_interior']
            leather_pipeline = Pipeline(
                steps=[('onehot', OneHotEncoder(drop='first'))]
            )

            # Combine the pipelines into a single ColumnTransformer
            preprocessor = ColumnTransformer(
                transformers=[
                    ("numeric_pipeline", numeric_pipeline, numeric_cols),
                    ("leather_pipeline", leather_pipeline, leather_interior_cols)
                ]
            )

            return preprocessor, numeric_cols, leather_interior_cols

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
            preprocessing_obj, numeric_cols, leather_interior_cols = self.get_data_transformer_object()

            # Apply transformations on train and test data
            train_df[numeric_cols + leather_interior_cols] = preprocessing_obj.fit_transform(train_df[numeric_cols + leather_interior_cols])
            test_df[numeric_cols + leather_interior_cols] = preprocessing_obj.transform(test_df[numeric_cols + leather_interior_cols])
            
            logging.info("Applied the preprocessing object on the training and testing dataframes.")

            for col in train_df.select_dtypes(include=['object']).columns:
                train_df[col] = train_df[col].astype('category')

            for col in test_df.select_dtypes(include=['object']).columns:
                test_df[col] = test_df[col].astype('category')
            
            # Save the preprocessing object
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (
                train_df, test_df, self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)
