from Customer_Segmentation_Retention_Strategy.config.configuration import ConfigurationManager
from Customer_Segmentation_Retention_Strategy.components.model_evaluation import ModelEvaluation
from Customer_Segmentation_Retention_Strategy.utils.logger import logger


STAGE_NAME = "Model Evaluation Stage"

class ModelEvaluationTrainingPipeline:

    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()
        model_evaluation = ModelEvaluation(config=model_evaluation_config)
        model_evaluation.evaluate()


if __name__ == "__main__":
    try:
        logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n")
        obj = ModelEvaluationTrainingPipeline()
        obj.main()
        logger.info(f"\n\n{'*'*20} {STAGE_NAME} completed {'*'*20}\n")
    except Exception as e:
        logger.exception(e)
        raise e