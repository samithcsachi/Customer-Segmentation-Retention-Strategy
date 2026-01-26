import os 
from pathlib import Path
import logging 


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


project_name = 'Customer_Segmentation_Retention_Strategy'


list_of_files = [

    f"SRC/{project_name}/__init__.py",
    f"SRC/{project_name}/components/__init__.py",
    f"SRC/{project_name}/components/data_ingestion.py",
    f"SRC/{project_name}/components/data_validation.py",
    f"SRC/{project_name}/components/data_transformation.py",
    f"SRC/{project_name}/components/model_trainer.py",
    f"SRC/{project_name}/components/model_evaluation.py",
    f"SRC/{project_name}/components/model_monitoring.py",
    f"SRC/{project_name}/components/model_maintenance.py",
    f"SRC/{project_name}/utils/__init__.py",
    f"SRC/{project_name}/utils/common.py",
    f"SRC/{project_name}/config/__init__.py",
    f"SRC/{project_name}/config/configuration.py",
    f"SRC/{project_name}/pipelines/__init__.py",
    f"SRC/{project_name}/pipelines/stage_01_data_ingestion.py",
    f"SRC/{project_name}/pipelines/stage_02_data_validation.py",
    f"SRC/{project_name}/pipelines/stage_03_data_transformation.py",
    f"SRC/{project_name}/pipelines/stage_04_model_trainer.py",
    f"SRC/{project_name}/pipelines/stage_05_model_evaluation.py",
    f"SRC/{project_name}/pipelines/stage_06_model_monitoring.py",   
    f"SRC/{project_name}/pipelines/stage_07_model_maintenance.py",
    f"SRC/{project_name}/entity/__init__.py",
    f"SRC/{project_name}/entity/config_entity.py",
    f"SRC/{project_name}/constants/__init__.py",
    "config/config.yaml",
    "params.yaml",
    "research/01_exploratory_analysis_and_business_insights.ipynb",
    "research/02_customer_churn_prediction_model.ipynb",
    
]

for file_path in list_of_files:
    file_path = Path(file_path)
    file_dir, filename = os.path.split(file_path)
   
    if file_dir !="":
        os.makedirs(file_dir, exist_ok=True)
        logging.info(f"Created directory: {file_dir} for the file: {filename}")
    
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        with open(file_path, 'w') as f:
            pass
        logging.info(f"Created empty file: {file_path}")

    else:
        logging.info(f"File already exists: {file_path} and is not empty.")
        