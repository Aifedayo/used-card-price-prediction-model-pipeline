import os
import sys
from dataclasses import dataclass

import pandas as pd
import numpy as np

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object, evaluate_models, train_test_cross_validate


@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and test input data")

            # Ensure that train_array and test_array are pandas DataFrames
            if isinstance(train_array, np.ndarray):
                train_array = pd.DataFrame(train_array)
            if isinstance(test_array, np.ndarray):
                test_array = pd.DataFrame(test_array)

            X_train, y_train = train_array.iloc[:, 1:], train_array.iloc[:, 0]
            X_test, y_test = test_array.iloc[:, 1:], test_array.iloc[:, 0]

            model_params = {
                'linear_regression': {
                    'model': LinearRegression(),
                    'params': {
                        'n_jobs': [1, 2, 5]
                    }
                },
                'random_forest_reg': {
                    'model': RandomForestRegressor(),
                    'params': {
                        'max_depth': [150],
                        'n_estimators': [150, 200],
                    }
                },
                'xgb_regressor': {
                    'model': XGBRegressor(objective='reg:squarederror', enable_categorical=True),
                    'params': {
                        'n_estimators': [150, 200]
                    }
                },
                'catboost_regressor': {
                    'model': CatBoostRegressor(),
                    'params': {
                        'depth': [6,8,10],
                        'learning_rate': [0.01, 0.05, 0.1],
                        'iterations': [30, 50, 100]
                    }
                }
            }

            additional_params = {
                'X_train': X_train,
                'y_train': y_train,
                'X_test': X_test,
                'y_test': y_test,
                'cv': 10
            }

            model_report: dict = evaluate_models(X_train, y_train, model_params)
            print(model_report)
            logging.info(f"Model evaluation report: {model_report}")

            # Get the best model based on evaluation score
            best_models = model_report.sort_values(by='best_score', ascending=False)
            best_model = dict(best_models.iloc[0,:].items())
            best_model_params = best_model['best_params']

            logging.info(f"Best model found: {best_model} with parameters: {best_model_params}")

            # Re-instantiate the best model with the best found parameters
            best_model_instance = model_params[best_model['model_name']]['model'].set_params(**best_model_params)

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model_instance
            )

            # Train and cross-validate the best model
            logging.info(f"Training and cross-validating the best model: {best_model}")
            trained_model = train_test_cross_validate(best_model_instance, **additional_params)

            logging.info(f"Best model trained: {trained_model}")

            # Predictions and performance evaluation
            predicted = best_model_instance.predict(X_test)

            r2_square = r2_score(y_test, predicted)
            logging.info(f"R2 score for the best model on test set: {r2_square}")

            return r2_square
    

        except Exception as e:
            raise CustomException(e, sys)
