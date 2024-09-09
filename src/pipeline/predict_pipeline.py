import sys
import pandas as pd
import numpy as np
import json
import joblib

from src.exception import CustomException
from src.logger import logging
from src.utils import load_object, load_json_object, get_value_from_dict


manufacturers_dict = load_json_object('artifacts/Manufacturer.json')
models_dict = load_json_object('artifacts/Model.json')
categories_dict = load_json_object('artifacts/Category.json')
fuel_types_dict = load_json_object('artifacts/Fuel_type.json')
gear_box_types_dict = load_json_object('artifacts/Gear_box_type.json')
drive_wheels_dict = load_json_object('artifacts/Drive_wheels.json')
colors_dict = load_json_object('artifacts/Color.json')


class PredictPipeline:
    def __init__(self) -> None:
        pass
        
    def predict_used_car_price(self, **kwargs):
        """Util function to predict the price of a used car."""

        feature_columns = load_json_object('artifacts/columns.json')
        mileage_scaler = joblib.load('artifacts/mileage_scaler.pkl')
        model = joblib.load('artifacts/model.pkl')
        x = np.zeros(len(feature_columns['data_columns']))
        
        for key, value in kwargs.items():
            
            if key == 'levy':
                x[0] = value
            
            elif key == 'manufacturer':
                x[1] = get_value_from_dict(value, manufacturers_dict['Manufacturers'])
            
            elif key == 'model':
                x[2] = get_value_from_dict(value, models_dict['Models'])
            
            elif key == 'prod_year':
                x[3] = value
            
            elif key == 'category':
                x[4] = get_value_from_dict(value, categories_dict['Categorys'])
            
            elif key == 'interior':
                x[5] = 1 if value == 'Leather' else 0
            
            elif key == 'fuel_type':
                x[6] = get_value_from_dict(value, fuel_types_dict['Fuel_types'])
            
            elif key == 'engine_volume':
                x[7] = value
            
            elif key == 'mileage':
                mileage_df = pd.DataFrame([[value]], columns=['Mileage'])
                x[8] = mileage_scaler.transform(mileage_df)[0][0]
            
            elif key == 'cylinder':
                x[9] = value
            
            elif key == 'gear_box_type':
                x[10] = get_value_from_dict(value, gear_box_types_dict['Gear_box_types'])
            
            elif key == 'drive_wheel':
                x[11] = get_value_from_dict(value, drive_wheels_dict['Drive_wheelss'])
            
            elif key == 'color':
                x[12] = get_value_from_dict(value, colors_dict['Colors'])
            
            elif key == 'airbag':
                x[13] = value
        
        x_df = pd.DataFrame([x], columns=feature_columns['data_columns'])
        return model.predict(x_df)[0]
    

class CustomData:
    def __init__(self):
        pass


if __name__ == '__main__':
    predict = PredictPipeline()
    print(predict.predict_used_car_price(
        levy=1234,
        manufacturer='HonDa', 
        model='Civic', 
        category='sedan',
        prod_year=2018, 
        fuel_type='Petrol', 
        color='Yellow', 
        engine_volume=3.5, 
        drive_wheel='4x4', 
        airbag=10, 
        cylinder=12, 
        mileage=145000, 
        interior='Leather'))