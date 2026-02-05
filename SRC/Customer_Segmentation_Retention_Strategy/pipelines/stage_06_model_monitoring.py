from Customer_Segmentation_Retention_Strategy.config.configuration import ConfigurationManager
from Customer_Segmentation_Retention_Strategy.components.model_monitoring import ModelMonitoring
from Customer_Segmentation_Retention_Strategy.utils.logger import logger


STAGE_NAME = "Model Monitoring Stage"

class ModelMonitoringTrainingPipeline:

    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_monitoring_config = config.get_model_monitoring_config()
        model_monitoring = ModelMonitoring(config=model_monitoring_config)
        model_monitoring.run_monitoring()


if __name__ == "__main__":
    try:
        logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n")
        obj = ModelMonitoringTrainingPipeline()
        obj.main()
        logger.info(f"\n\n{'*'*20} {STAGE_NAME} completed {'*'*20}\n")
    except Exception as e:
        logger.exception(e)
        raise e