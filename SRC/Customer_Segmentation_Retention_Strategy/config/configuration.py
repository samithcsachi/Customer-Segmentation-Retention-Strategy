import os
from pathlib import Path
from Customer_Segmentation_Retention_Strategy.constants import  *
from Customer_Segmentation_Retention_Strategy.utils.common import read_yaml, create_directories
from Customer_Segmentation_Retention_Strategy.entity.config_entity import (DataIngestionConfig,DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig,ModelMonitoringConfig,ModelMaintenanceConfig)

class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH,
        schema_filepath = SCHEMA_FILE_PATH):

        current_file = Path(__file__)
        self.project_root = current_file.parent.parent.parent.parent

   
        config_filepath = self.project_root / config_filepath
        params_filepath = self.project_root / params_filepath
        schema_filepath = self.project_root / schema_filepath

     
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
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


    def get_model_trainer_config(self) -> ModelTrainerConfig: 
        config = self.config.model_trainer
        params = self.params
        xgb_params = params.XGBOOST
        training_params = params.TRAINING
        schema = self.schema.TARGET_COLUMN

        root_dir_path = self.project_root / self.config.artifacts_root / "model_trainer"
        create_directories([str(root_dir_path)])

        model_trainer_config = ModelTrainerConfig(
        root_dir=self.project_root / Path(config.root_dir),
        train_data_path=config.train_data_path,
            test_data_path=config.test_data_path,
            data_transformation_dir=self.config.data_transformation.root_dir, 
            model_name=config.model_name,
            target_column=schema.name,
            
            objective=xgb_params.objective,
            n_estimators=xgb_params.n_estimators,
            learning_rate=xgb_params.learning_rate,
            max_depth=xgb_params.max_depth,
            subsample=xgb_params.subsample,
            colsample_bytree=xgb_params.colsample_bytree,
            min_child_weight=xgb_params.min_child_weight,
            random_state=xgb_params.random_state,

            eval_metric=training_params.eval_metric

        )
        return model_trainer_config
    

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config.model_evaluation
        schema = self.schema.TARGET_COLUMN

        root_dir_path = self.project_root / self.config.artifacts_root / "model_evaluation"
        create_directories([config.root_dir])

        model_evaluation_config = ModelEvaluationConfig(
            root_dir=config.root_dir,
            test_data_path=config.test_data_path,
            model_path=config.model_path,
            report_path=config.report_path,
            target_column=schema.name
        )
        return model_evaluation_config
    

    def get_model_monitoring_config(self) -> ModelMonitoringConfig:
        config = self.config.model_monitoring

        root_dir_path = self.project_root / self.config.artifacts_root / "model_monitoring"
        create_directories([str(root_dir_path)])

        model_monitoring_config = ModelMonitoringConfig(
            root_dir=root_dir_path,
            baseline_data_path=self.project_root / Path(config.baseline_data_path),
            production_data_path=self.project_root / Path(config.production_data_path),
            psi_threshold=config.psi_threshold,
            drift_report_path=self.project_root / Path(config.drift_report_path)
        )

        return model_monitoring_config
    

    def get_model_maintenance_config(self) -> ModelMaintenanceConfig:
        config = self.config.model_maintenance

        root_dir_path = self.project_root / self.config.artifacts_root / "model_maintenance"
        create_directories([str(root_dir_path)])

        model_maintenance_config = ModelMaintenanceConfig(
            root_dir=root_dir_path,
            model_registry_path=self.project_root / Path(config.model_registry_path),
            retrain_on_drift=config.retrain_on_drift,
            retrain_mode=config.retrain_mode
        )

        return model_maintenance_config