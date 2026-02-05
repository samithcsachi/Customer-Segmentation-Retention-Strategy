from Customer_Segmentation_Retention_Strategy.config.configuration import ConfigurationManager
from Customer_Segmentation_Retention_Strategy.components.model_maintenance import ModelMaintenance
from Customer_Segmentation_Retention_Strategy.utils.logger import logger


STAGE_NAME = "Model Maintenance Stage"

class ModelMaintenanceTrainingPipeline:

    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()

        monitoring_config = config.get_model_monitoring_config()
        maintenance_config = config.get_model_maintenance_config()
        

        model_maintenance = ModelMaintenance(
            monitoring_config=monitoring_config,
            maintenance_config=maintenance_config
        )
        model_maintenance.retrain_decision()


if __name__ == "__main__":
    try:
        logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n")
        obj = ModelMaintenanceTrainingPipeline()
        obj.main()
        logger.info(f"\n\n{'*'*20} {STAGE_NAME} completed {'*'*20}\n")
    except Exception as e:
        logger.exception(e)
        raise e