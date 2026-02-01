import os
import shutil
from Customer_Segmentation_Retention_Strategy.utils.logger import logger
from Customer_Segmentation_Retention_Strategy.utils.common import get_size
from Customer_Segmentation_Retention_Strategy.entity.config_entity import DataIngestionConfig
from pathlib import Path

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self) -> str:

        try:
    
            project_root = Path(__file__).parent.parent.parent.parent
            
            root_dir = Path(self.config.root_dir)
            root_dir.mkdir(parents=True, exist_ok=True)
            
      
            readings_source = project_root / self.config.local_data_file
            readings_dest = root_dir / readings_source.name
            
            if readings_source.exists():
                shutil.copy2(str(readings_source), str(readings_dest))
                logger.info(f"Files copied successfully")
            else:
                logger.warning(f" File not found: {readings_source}")
            
        

            
        except Exception as e:
            logger.error(f"Failed to copy files: {e}")
            raise
    