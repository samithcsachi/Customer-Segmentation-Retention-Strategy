import os
from pathlib import Path
from Customer_Segmentation_Retention_Strategy.constants import  *
from Customer_Segmentation_Retention_Strategy.utils.common import read_yaml, create_directories
from Customer_Segmentation_Retention_Strategy.entity.config_entity import (DataIngestionConfig)

class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):

        current_file = Path(__file__)
        self.project_root = current_file.parent.parent.parent.parent
        config_filepath = self.project_root / "config" / "config.yaml"
        self.config = read_yaml(config_filepath)
        #self.params = read_yaml(params_filepath)
        

        artifacts_root = self.project_root / self.config.artifacts_root
        create_directories([str(artifacts_root)])


    def get_data_ingestion_config(self) -> DataIngestionConfig:

        config = self.config.data_ingestion
        

        root_dir_path = self.project_root / self.config.artifacts_root / "data_ingestion"
        create_directories([str(root_dir_path)])
        
        data_ingestion_config = DataIngestionConfig(
            root_dir= str(root_dir_path),
            local_data_file_reading=config.local_data_files.readings,
            local_data_file_users=config.local_data_files.users,
        )
        return data_ingestion_config