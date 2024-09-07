import os
import sys

from dataclasses import dataclass

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def rename_columns_with_underscore(self):
        pass

    def remove_outlier(self):
        pass

    def get_data_transformer_object(self):
        """
        This function is responsible for data transformation
        """
        try:
            pass

        except Exception as e:
            raise CustomException(e, sys)