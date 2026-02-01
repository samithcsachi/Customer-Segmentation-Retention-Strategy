import os
from pathlib import Path
from Customer_Segmentation_Retention_Strategy.constants import  *
from Customer_Segmentation_Retention_Strategy.utils.common import read_yaml, create_directories
from Customer_Segmentation_Retention_Strategy.entity.config_entity import (DataIngestionConfig,DataValidationConfig, DataTransformationConfig)

class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH,
        schema_filepath = SCHEMA_FILE_PATH):

        current_file = Path(__file__)
        self.project_root = current_file.parent.parent.parent.parent

   
        config_filepath = self.project_root / config_filepath
        #params_filepath = self.project_root / params_filepath
        schema_filepath = self.project_root / schema_filepath

     
        self.config = read_yaml(config_filepath)
        #self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)
        

        artifacts_root = self.project_root / self.config.artifacts_root
        create_directories([str(artifacts_root)])


    def get_data_ingestion_config(self) -> DataIngestionConfig:

        config = self.config.data_ingestion
        

        root_dir_path = self.project_root / self.config.artifacts_root / "data_ingestion"
        create_directories([str(root_dir_path)])
        
        data_ingestion_config = DataIngestionConfig(
            root_dir=root_dir_path,
            local_data_file=self.project_root / Path(config.local_data_file),

        )

        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        schema = self.schema.COLUMNS
        root_dir_path = self.project_root / self.config.artifacts_root / "data_validation"
        create_directories([str(root_dir_path)])

        data_validation_config = DataValidationConfig(
            root_dir=self.project_root / Path(config.root_dir),           
            STATUS_FILE=self.project_root / Path(config.STATUS_FILE),
            source_file_path=self.project_root / Path(config.source_file_path),
            all_schema=schema
        )
        return data_validation_config

    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation

        root_dir_path = self.project_root / self.config.artifacts_root / "data_transformation"
        create_directories([str(root_dir_path)])


        data_transformation_config = DataTransformationConfig(
        root_dir=self.project_root / Path(config.root_dir),
        source_file_path=self.project_root / Path(config.source_file_path)
        
        )

   
        return data_transformation_config