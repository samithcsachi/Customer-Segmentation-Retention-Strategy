from Customer_Segmentation_Retention_Strategy.config.configuration import ConfigurationManager
from Customer_Segmentation_Retention_Strategy.components.data_validation import DataValidation
from Customer_Segmentation_Retention_Strategy.utils.logger import logger

STAGE_NAME = "Data Validation Stage"

class DataValidationTrainingPipeline():
    def _init__(self):
        pass 

    def main(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(config=data_validation_config)
        data_validation.validate_all_columns()



if __name__ == "__main__":
    try:
        logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n")
        obj = DataValidationTrainingPipeline()
        obj.main()
        logger.info(f"\n\n{'*'*20} {STAGE_NAME} completed {'*'*20}\n")
    except Exception as e:
        logger.exception(e)
        raise e