import os
import sys
from dataclasses import dataclass

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
    trained_model_file_path=os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()


    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Split training and test input data")
            X_train, y_train = train_array.iloc[:, :-1], train_array.iloc[:, -1]
            X_test, y_test = test_array.iloc[:, :-1], test_array.iloc[:, -1]

            model_params = {
                'linear_regression': {
                    'model': LinearRegression(),
                    'params': {
                        'n_jobs': [5,10]
                    }
                },
                'random_forest_reg': {
                    'model': RandomForestRegressor(),
                    'params': {
                        'max_depth': [150],
                        'n_estimators': [300],
                    }
                },
                'xgb_regressor': {
                    'model': XGBRegressor(objective='reg:squarederror', enable_categorical=True),
                    'params': {
                        'n_estimators': [200]
                    }
                }
            }

            model_report:dict=evaluate_models(X_train, y_train)
            
            ## To get best model score from dict
            best_model_score = max(sorted(model_report.values()))

            


            if best_model_score<0.6:
                raise CustomException("No best model found")
            logging.info(f"Best found model on both training and testing dataset")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            additional_params = {
                'X_train' : X_train, 
                'y_train' : y_train, 
                'X_test' : X_test, 
                'y_test': y_test, 
                'cv':10
            }
            for model_name, model in models.items():
                print(f'{model_name} Regression Model: ')
                print()

                trained_model = train_test_cross_validate(model, **additional_params)

                print(trained_model)




            predicted=best_model.predict(X_test)

            r2_square = r2_score(y_test, predicted)
            return r2_square
            
        except Exception as e:
            raise CustomException(e,sys)