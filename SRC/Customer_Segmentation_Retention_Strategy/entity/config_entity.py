from dataclasses import dataclass
from pathlib import Path
from typing import List
from typing import Dict



@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    local_data_file: Path

@dataclass(frozen=True)
class DataValidationConfig:
    
    root_dir: Path
    STATUS_FILE: str
    source_file_path : Path
    all_schema: dict



@dataclass(frozen=True)
class DataTransformationConfig:
    
    root_dir: Path
    source_file_path: Path


@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    data_transformation_dir: Path  
    model_name: str
    target_column: str

    objective: str
    n_estimators: int
    learning_rate: float
    max_depth: int
    subsample: float
    colsample_bytree: float
    min_child_weight: int
    random_state: int

    eval_metric: str


@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    test_data_path: Path
    model_path: Path
    report_path: Path  
    target_column: str

@dataclass(frozen=True)
class ModelMonitoringConfig:
    root_dir: Path
    baseline_data_path: Path
    production_data_path: Path
    psi_threshold: float
    drift_report_path: Path

@dataclass(frozen=True)
class ModelMaintenanceConfig:
    root_dir: Path
    model_registry_path: Path
    retrain_on_drift: bool
    retrain_mode: str