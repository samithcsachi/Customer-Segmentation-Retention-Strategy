from Customer_Segmentation_Retention_Strategy.utils.logger import logger
from Customer_Segmentation_Retention_Strategy.pipelines.stage_01_data_ingestion import DataIngestionTrainingPipeline



STAGE_NAME = "Data Ingestion Stage"


try:
    logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.main()
    logger.info(f"\n\n{'*'*20} {STAGE_NAME} completed {'*'*20}\n")
except Exception as e:
    logger.exception(e)
    raise e