import os
from MLOPS_project import logger
from MLOPS_project.entity.config_entity import DataValidationConfig
import pandas as pd


class DataValiadtion:
    def __init__(self, config: DataValidationConfig):
        self.config = config


    def validate_all_columns(self)-> bool:
        try:
            validation_status = None

            data = pd.read_csv(self.config.unzip_data_dir)
            data['type'] = data['type'].map({'red': 1, 'white': 0})

            cols_to_fill = ["fixed acidity", "volatile acidity", "citric acid", "residual sugar", "chlorides", "pH", "sulphates"]
            for col in cols_to_fill:  
                data[col] = data[col].fillna(data[col].mean())
            
            data['type'] = pd.to_numeric(data['type'], errors='coerce')

            all_cols = list(data.columns)

            all_schema = self.config.all_schema.keys()

            
            for col in all_cols:
                if col not in all_schema:
                    validation_status = False
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"Validation status: {validation_status}")
                else:
                    validation_status = True
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"Validation status: {validation_status}")

            return validation_status
        
        except Exception as e:
            raise e
