import os
import sys
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

# Utility functions
def isInt(x):
    try:
        return int(x)
    except:
        return None

def convert_cols_to_int(df, cols:list):
    for col in cols:
        df[col] = df[col].apply(isInt)
        if df[col].isna().sum() > 0:
            df[col] = df[col].fillna(df[col].mean())
        df[col] = df[col].astype(int)

def drop_columns(df, cols:list):
    return df.drop(cols, axis=1)

def get_and_remove_outliers(col, df):
    lower_limit, upper_limit = df[col].quantile([0.05, 0.95])
    df = df[(df[col] <= upper_limit) & (df[col] >= lower_limit)]
    return df

def encoded_cols(df, cols_to_encode:list):
    for col in cols_to_encode:
        json_name = col + 's'
        mean_price = df.groupby(col)['Price'].mean()
        sorted_col = mean_price.sort_values(ascending=True)
        col_encoding = {column: value + 1 for value, column in enumerate(sorted_col.index)}

        col_name = {json_name: col_encoding}
        json_path = os.path.join('artifacts', f'{col}.json')
        os.makedirs(os.path.dirname(json_path), exist_ok=True)

        with open(json_path, 'w') as file:
            json.dump(col_name, file, indent=4)

        df[col] = df[col].map(col_encoding)
    return df


# Data ingestion class
@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info('Entered the data ingestion method')
        try:
            # Read the data as a csv file into df
            df = pd.read_csv('notebook/data/car_price_prediction.csv')
            logging.info('Read the datasets as a dataframe')

            # Dataframe cleaning
            df.columns = df.columns.str.replace(' ', '_')
            df.Mileage = df.Mileage.apply(lambda x: x.split()[0])
            df.Engine_volume = df.Engine_volume.str.split(' ').str[0].astype(float)

            # Feature engineering
            df = self.feature_engineering(df)

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            # Split the data
            return self.split_data(df)

        except Exception as e:
            raise CustomException(e, sys)

    def feature_engineering(self, df):
        cols_to_convert = ['Levy', 'Mileage', 'Cylinders']
        convert_cols_to_int(df, cols_to_convert)

        cols_to_drop = ['ID', 'Doors', 'Wheel']
        df = drop_columns(df, cols_to_drop)

        df = get_and_remove_outliers('Mileage', df)
        df = get_and_remove_outliers('Engine_volume', df)
        df = get_and_remove_outliers('Levy', df)

        cols_to_encode = ['Manufacturer', 'Model', 'Category', 'Gear_box_type', 'Fuel_type', 'Color', 'Drive_wheels']
        df = encoded_cols(df, cols_to_encode)
        
        return df

    def split_data(self, df):
        train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
        train_set.to_csv(self.ingestion_config.train_data_path, header=True, index=False)
        test_set.to_csv(self.ingestion_config.test_data_path, header=True, index=False)
        logging.info("Ingestion of data completed!")
        return (
            self.ingestion_config.train_data_path,
            self.ingestion_config.test_data_path
        )

if __name__ == '__main__':
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data)

    model_trainer = ModelTrainer()
    print(model_trainer.initiate_model_trainer(train_arr, test_arr))
