import os
import sys

from dataclasses import dataclass

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        This function is responsible for creating a pipeline
        that will transform the data.
        """
        try:
            # Pipeline for scaling numerical features
            numeric_cols = ['Mileage']
            numeric_pipeline = Pipeline(
                steps=[
                    ("scaler", StandardScaler())
                ]
            )

            # Pipeline for encoding categorical features
            leather_interior = ['Leather_interior']
            leather_pipeline = Pipeline(
                steps=[
                    ('onehot', OneHotEncoder(drop='first'))
                ]
            )

            # Combine the pipelines into a single ColumnTransformer
            preprocessor = ColumnTransformer([
                ("numeric_pipeline", numeric_pipeline, numeric_cols),
                ("leather_pipeline", leather_pipeline, leather_interior)
            ])

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)