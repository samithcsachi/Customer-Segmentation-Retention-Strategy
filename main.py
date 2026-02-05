from Customer_Segmentation_Retention_Strategy.utils.logger import logger
from Customer_Segmentation_Retention_Strategy.pipelines.stage_01_data_ingestion import DataIngestionTrainingPipeline
from Customer_Segmentation_Retention_Strategy.pipelines.stage_02_data_validation import DataValidationTrainingPipeline
from Customer_Segmentation_Retention_Strategy.pipelines.stage_03_data_transformation import DataTransformationTrainingPipeline
from Customer_Segmentation_Retention_Strategy.pipelines.stage_04_model_trainer import ModelTrainerTrainingPipeline
from Customer_Segmentation_Retention_Strategy.pipelines.stage_05_model_evaluation import ModelEvaluationTrainingPipeline
from Customer_Segmentation_Retention_Strategy.pipelines.stage_06_model_monitoring import ModelMonitoringTrainingPipeline
from Customer_Segmentation_Retention_Strategy.pipelines.stage_07_model_maintenance import ModelMaintenanceTrainingPipeline




STAGE_NAME = "Data Ingestion Stage"


try:
    logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.main()
    logger.info(f"\n\n{'*'*20} {STAGE_NAME} completed {'*'*20}\n")
except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME = "Data Validation Stage"

try:
    logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n")
    data_validation = DataValidationTrainingPipeline()
    data_validation.main()
    logger.info(f"\n\n{'*'*20} {STAGE_NAME} completed {'*'*20}\n")
except Exception as e:
    logger.exception(e)
    raise e 




STAGE_NAME = "Data Transformation Stage"

try:
    logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n")
    data_transformation = DataTransformationTrainingPipeline()
    data_transformation.main()
    logger.info(f"\n\n{'*'*20} {STAGE_NAME} completed {'*'*20}\n")
except Exception as e:
    logger.exception(e)
    raise e 


STAGE_NAME = "Model Trainer Stage"

try:
    logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n")
    model_trainer = ModelTrainerTrainingPipeline()
    model_trainer.main()
    logger.info(f"\n\n{'*'*20} {STAGE_NAME} completed {'*'*20}\n")
except Exception as e:
    logger.exception(e)
    raise e 


STAGE_NAME = "Model Evaluation Stage"

try:
    logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n")
    model_evaluation = ModelEvaluationTrainingPipeline()
    model_evaluation.main()
    logger.info(f"\n\n{'*'*20} {STAGE_NAME} completed {'*'*20}\n")
except Exception as e:
    logger.exception(e)
    raise e 


STAGE_NAME = "Model Monitoring Stage"

try:
    logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n")
    model_monitoring = ModelMonitoringTrainingPipeline()
    model_monitoring.main()
    logger.info(f"\n\n{'*'*20} {STAGE_NAME} completed {'*'*20}\n")
except Exception as e:
    logger.exception(e)
    raise e 



STAGE_NAME = "Model Maintenance Stage"

try:
    logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n")
    model_maintenance = ModelMaintenanceTrainingPipeline()
    model_maintenance.main()
    logger.info(f"\n\n{'*'*20} {STAGE_NAME} completed {'*'*20}\n")
except Exception as e:
    logger.exception(e)
    raise e 