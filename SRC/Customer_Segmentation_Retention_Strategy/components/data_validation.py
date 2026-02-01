import os
from Customer_Segmentation_Retention_Strategy.utils.logger import logger
from Customer_Segmentation_Retention_Strategy.entity.config_entity import DataValidationConfig
from pathlib import Path
import pandas as pd


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config


    def validate_all_columns(self) -> bool:
        try:
            logger.info("Loading the Data for Validation")
            excel_path = self.config.source_file_path
            sheets = pd.read_excel(excel_path, sheet_name=None)
            df = pd.concat(sheets.values(), ignore_index=True)
            all_cols = list(df.columns)
            all_schema = self.config.all_schema.keys()
            
            for col in all_cols:
                if col not in all_schema:
                    validation_status = False
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"validation status: {validation_status}")
                else:
                    validation_status = True
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"validation status: {validation_status}")
            logger.info(f"All columns validation status: {validation_status}")
            return validation_status
        except Exception as e:
            raise e