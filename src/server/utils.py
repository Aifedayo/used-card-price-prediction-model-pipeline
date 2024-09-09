import json
import joblib
import numpy as np
import pandas as pd

# Global variables
_artifacts = {
    "manufacturers": None,
    "models": None,
    "categories": None,
    "colors": None,
    "fuels": None,
    "gear_boxes": None,
    "drive_wheels": None,
    "manufacturers_columns": None,
    "models_columns": None,
    "categories_columns": None,
    "colors_columns": None,
    "fuel_types_columns": None,
    "gear_box_types_columns": None,
    "drive_wheels_columns": None,
    "data_columns": None,
    "manufacturers_to_models_columns": None,
    'scaler': None,
    "model_xgb": None,
    "model_rfr": None
}