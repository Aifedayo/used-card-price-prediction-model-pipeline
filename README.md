
# Used Car Price Prediction Model

## Overview

This project involves building a machine learning model to predict the price of used cars. The pipeline includes data ingestion, preprocessing, model training, evaluation, and prediction. The models used in this project include linear regression, random forest, XGBoost, and CatBoost. The best model is selected based on cross-validated performance metrics and then saved for future predictions.

## Project Structure

```
├── src/
│   ├── __init__.py
│   ├── logger.py
│   ├── exception.py
│   ├── utils.py
│   ├── server.py
├── components/
│   └── data_ingestion.py
│   └── data_preprocessing.py
│   └── model_trainer.py
│   └── prediction.py
├── artifacts/
│   └── model.pkl
|   └── preprocessor.pkl
├── pipelinw/
│   └── predict_pipeline.py
|   └── train_pipeline.py
├── notebooks/
│   └── car_price_prediction_v2.ipynb
├── data/
│   └── car_price_prediction.csv
├── README.md
├── setup.py
└── requirements.txt
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/used-car-price-prediction.git
   ```
2. Navigate to the project directory:
   ```bash
   cd used-car-price-prediction
   ```
3. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## How to Use

### Data Ingestion

The `data_ingestion.py` script is responsible for reading raw data, performing initial checks, and saving the processed data for model training.

### Data Preprocessing

The `data_preprocessing.py` script handles the data cleaning, feature engineering, and splitting into training and test datasets. This step is critical as it ensures that the model receives properly formatted and relevant data.

### Model Training

The `model_trainer.py` script performs the following tasks:
- It defines a configuration for model training.
- Splits the training and test data.
- Trains multiple models (e.g., Linear Regression, Random Forest, XGBoost, CatBoost) with cross-validation.
- Evaluates the models using a custom `evaluate_models` function.
- Selects the best model based on performance metrics.
- Saves the trained model to the `artifacts` directory.

### Prediction

The `prediction.py` script can be used to make predictions on new data using the trained model. Simply load the data and run the prediction pipeline.

### Logging

Logging is implemented using the `logging` module and is configured in `logger.py`. All important events, such as data loading, model training, and errors, are logged for easy debugging and tracking.

### Custom Exception Handling

Custom exceptions are managed through the `exception.py` module, which wraps around the standard Python exceptions, providing more context and logging the error messages.

## Example Workflow

1. Run data ingestion:
   ```bash
   python src/data_ingestion.py
   ```
2. Run data preprocessing:
   ```bash
   python src/data_preprocessing.py
   ```
3. Train the model:
   ```bash
   python src/model_trainer.py
   ```
4. Make predictions:
   ```bash
   python src/prediction.py
   ```

## Results

The model is evaluated using the R-squared metric on the test dataset. The best model and its performance metrics are saved in the `artifacts` directory.
| Model_name | best_params | best_score |
| ---------- | -----------| --------- |
| linear_regression | {'n_jobs': 1}  |  0.443118 |
| random_forest_reg   |         {'max_depth': 150, 'n_estimators': 200}   | 0.806956 |
| xgb_regressor         |                     {'n_estimators': 200}  |  0.796459 |
| catboost_regressor  | {'depth': 10, 'iterations': 100, 'learning_rat... |   0.779112 |
