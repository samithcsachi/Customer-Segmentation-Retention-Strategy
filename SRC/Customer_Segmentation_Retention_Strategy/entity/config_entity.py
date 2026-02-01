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


