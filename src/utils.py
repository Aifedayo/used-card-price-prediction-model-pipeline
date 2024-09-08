import pickle
import os
import sys

import pandas as pd
import numpy as np

from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV, ShuffleSplit, cross_val_score
from sklearn.metrics import mean_absolute_error

from src.exception import CustomException
from src.logger import logging


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as file:
            pickle.dump(obj, file)

    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_models(X, y, model_params):
    try:
        scores = []
        cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=42)
        for model_name, mp in model_params.items():
            gs = GridSearchCV(mp['model'], mp['params'], cv=cv, return_train_score=False)
            gs.fit(X, y)
            scores.append({
                'model_name': model_name,
                'best_params': gs.best_params_,
                'best_score': gs.best_score_
            })
        best_model = pd.DataFrame(scores, columns=['model_name', 'best_params', 'best_score'])
        return best_model

    except Exception as e:
        raise CustomException(e, sys)
    

def train_test_cross_validate(model, X_train, y_train, X_test, y_test, cv):
    try:
        model.fit(X_train, y_train)
        model_score = model.score(X_test, y_test)
        
        # Train pred
        y_train_pred = model.predict(X_train)
        rmse_train = mean_absolute_error(y_train, y_train_pred)

        # Test Pred
        y_test_pred = model.predict(X_test)
        rmse_test = mean_absolute_error(y_test, y_test_pred)

        # Perform 5-fold cross-validation
        rmse_cv = -cross_val_score(model, X_train, y_train, scoring='neg_root_mean_squared_error', cv=cv)

        rmse_cv_mean = np.mean(rmse_cv)

        # Display results
        print(f'Model Score: {model_score:.4f}')
        print(f"Training RMSE: {rmse_train:.4f}")
        print()
        print(f"Initial Test RMSE: {rmse_test:.4f}")
        print()
        print(f"Average Cross-Validation RMSE: {rmse_cv_mean:.4f}")
        print()
        print(f"Cross-Validation Scores: {rmse_cv}\n")
        print()

    except Exception as e:
        raise CustomException(e, sys)
