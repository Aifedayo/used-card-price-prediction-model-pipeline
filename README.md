# Used Car Price Prediction Model Pipeline
This repository contains a comprehensive machine-learning pipeline for predicting used car prices. The project involves data preprocessing, feature engineering, model training, and evaluation using advanced regression techniques. Key features include:

- [x] Data Handling: In-depth data cleaning, outlier detection, and categorical encoding.

- [x] Feature Engineering: Customized feature extraction and transformation based on car attributes like Manufacturer, Model, Category, and more.
- [x] Modeling: Implementing state-of-the-art models, including XGBoost and RandomForestRegressor, with hyperparameter tuning.
- [x] Evaluation: Robust evaluation metrics and visualization for model performance comparison.
- [x] Web Interface: An HTML-based form allowing users to input car details and predict prices in real-time.

This pipeline is ideal for data enthusiasts, automotive analysts, and machine learning practitioners looking to explore predictive modeling in the automotive domain.


Data Ingestion Process
The data_ingestion.py script is responsible for the initial step in the machine learning pipeline: ingesting and preparing the raw data for further processing. This script performs several crucial tasks, including:

Data Loading:

The script begins by loading the raw dataset from a CSV file into a pandas DataFrame. The dataset is expected to contain various features related to car price prediction.
Data Cleaning:

Column Renaming: The columns are renamed to replace spaces with underscores for better readability and easier access.
Mileage Cleaning: The Mileage column is stripped of any unit suffixes to retain only the numerical values.
Engine Volume Conversion: The Engine_volume column, which contains both numerical values and units, is split to keep only the numerical part and convert it to a float.
Data Conversion:

The script includes a function (convert_cols_to_int) that converts specified columns to integer type after handling any missing values by imputing the mean.
Feature Engineering:

Encoding Categorical Variables: The categorical features such as Manufacturer, Model, Category, etc., are encoded using their mean price, and the mappings are saved as JSON files for reference.
Outlier Removal: The script identifies and removes outliers from specific numerical columns (Mileage, Engine_volume, and Levy) based on their 5th and 95th percentiles.
Data Splitting:

The cleaned and processed data is split into training and testing sets using an 80/20 ratio. The resultant datasets are saved as CSV files in the artifacts directory.
Error Handling:

Any exceptions that occur during the ingestion process are captured and handled using a custom exception class, ensuring that the script can log and report errors effectively.
This script is essential for ensuring that the raw data is clean, well-structured, and ready for the next stages of the machine learning pipeline, such as feature selection, model training, and evaluation.
